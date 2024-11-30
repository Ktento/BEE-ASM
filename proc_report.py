#!/usr/bin/env python3
import os
import urllib.request
import ssl
import json
import time
import requests
import smtplib
import csv
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from xml.dom import minidom
from datetime import datetime, timedelta
from context import Context
from log import Level
import config as Config
import xml.etree.ElementTree as ET
import urllib.parse

def review_description(description):
	# print(f"description: {description}")
	API_KEY = Config.ReportAPIKey
	END_POINT = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={API_KEY}"
	custom_txt = """
	依頼: CVEの説明を下記に記載するので、日本語で脆弱性評価をしてください。
	\n\n
	"""

	payload = {
		"contents": {
			"role": "user",
			"parts": {
				"text": custom_txt + description
			}
		}
	}
	headers = {
		"Content-Type": "application/json",
	}

	response = requests.post(END_POINT, headers=headers, json=payload)

	if response.status_code == 200:
		data = response.json()
		gemini_response = data["candidates"][0]["content"]["parts"][0]["text"]
		# print(f"AI Review: {gemini_response}")
		return gemini_response
	# else:
	# 	print(f"failed. http status code: {response.status_code}")
	# 	print("preview:", response.text)

def create_csvs(cveData, hostCpes, fAll, fPer):
	# 全ホストのCVE情報
	wa = csv.DictWriter(fAll, ["CPE", "CVEID", "CVSS3", "CVSS", "Published", "Description", "Gemini"])
	wa.writeheader()

	# ホストごとのCVE情報
	wp = csv.DictWriter(fPer, ["Host", "CPE", "CVEID", "CVSS3", "CVSS", "Published", "Description", "Gemini"])
	wp.writeheader()

	dic = dict()
	for cve in cveData:
		d = {
			"CPE": cve["cpe"],
			"CVEID": cve["id"],
			"CVSS3": str.format("{:.1f}", cve["cvss3"]),
			"CVSS": str.format("{:.1f}", cve["cvss"]),
			"Published":  cve["published_str"],
			"Description":  cve["summary"],
			"Gemini": cve["gemini"],
		}
		wa.writerow(d)

		if cve["cpe"] in dic:
			dic[cve["cpe"]].append(d)
		else:
			dic[cve["cpe"]] = [d]

	for hostCpe in hostCpes:
		for cpe in hostCpe[1]:
			if cpe not in dic: continue
			for i in dic[cpe]:
				i["Host"] = hostCpe[0]
				wp.writerow(i)

def send_email(ctx, body, attachments):
	# 送信元や宛先など
	from_email = Config.ReportFrom
	to_email = ""
	cc_mail = str.join(",", Config.ReportEmails)
	mail_title = "ASMツール実行のお知らせ"
	message = body

	#  MIMEオブジェクトでメールを作成
	msg = MIMEMultipart()
	msg["Subject"] = mail_title
	msg["From"] = from_email
	msg["To"] = to_email
	msg["Bcc" if Config.ReportEnableBCC else "Cc"] = cc_mail

	# 本文の添付
	msg.attach(MIMEText(message, "html", "utf-8"))

	# ファイル添付
	for att in attachments:
		try:
			with open(att, "rb") as f:
				p = MIMEApplication(f.read())
			# ASCII文字のみでエンコーディングできるならfilenameを付加する
			try:
				# ダブルクォート(")はアンダースコア(_)で置き換える
				fn1 = os.path.basename(att).replace('"', "_").encode("ascii")
				fn1.repl
				fn1 = 'filename=\"{fn1}\"; '
			except:
				fn1 = ""

			# RFC 5987形式のファイル名(filename*)
			fn2 = urllib.parse.quote(os.path.basename(att), encoding="utf-8")
			p.add_header("Content-Disposition", f"attachment; {fn1}filename*=UTF-8''{fn2}")
			msg.attach(p)
		except Exception as e:
			ctx.logger.Log(Level.ERROR, f'[Report] Failed to attach file "{att}": {e}')

	# サーバを指定してメールを送信する
	smtp_host = 'smtp.gmail.com'
	smtp_port = 587
	smtp_password = 'efbw jvxw mrnc cvdm'

	server = None
	try:
		server = smtplib.SMTP(smtp_host, smtp_port)
		server.starttls()
		server.login(from_email, smtp_password)
		server.send_message(msg)
		# print("メールが送信されました。")
	except smtplib.SMTPAuthenticationError as e:
		ctx.logger.Log(Level.ERROR, f"[Report] 認証エラー: {e}")
	except Exception as e:
		ctx.logger.Log(Level.ERROR, f"[Report] エラーが発生しました: {e}")
	finally:
		if server != None: server.quit()

def makereport(context: Context, cve_data_array, host_cpes):
	context.logger.Log(Level.INFO, f"[Report] Getting CVE information...")

	# 諸条件に一致するCVE情報のみ抽出する
	cve_data_array = filtering_cves(cve_data_array)
	for c in cve_data_array:
		c["gemini"] = "(Not permitted)"

	# Gemini有効時、抽出したものをレビューしてもらう
	if Config.EnableGemini:
		for c in cve_data_array[:Config.ReportLimit]:
			try:
				c["gemini"] = review_description(c["summary"])
			except Exception as e:
				c["gemini"] = "(Failed)"

	# HTML文書作成
	html = mkhtml(context, cve_data_array, host_cpes)
	try:
		with open(f"{context.savedir}/cve_report.html", "wb") as f: f.write(html)
	except Exception as e:
		context.logger.Log(Level.ERROR, f"[Report] Failed to write the HTML report to file: {e}")

	# 全ホストのCVEを格納するCSVのファイル名
	csv_filename_all = f"{context.savedir}/cve_report_all.csv"
	# ホストごとのCVEを格納するCSVのファイル名
	csv_filename_per = f"{context.savedir}/cve_report_per.csv"

	# CSVファイルの作成
	with open(csv_filename_all, mode='w', newline='', encoding=Config.ReportCSVEncoding) as csvfile_all, \
		open(csv_filename_per, mode='w', newline='', encoding=Config.ReportCSVEncoding) as csvfile_per:
		create_csvs(cve_data_array, host_cpes, csvfile_all, csvfile_per)

	# CSVを添付してEメール送信
	context.logger.Log(Level.INFO, f"[Report] Sending mail...")
	send_email(context, html, [csv_filename_all, csv_filename_per])
	context.logger.Log(Level.INFO, f"[Report] Mail sent.")

	# Optional: Remove the CSV file after sending the email
	# for name in [csv_filename_all, csv_filename_per]:
	# 	try:
	# 		os.remove(name)
	# 		context.logger.Log(Level.INFO, f"[Report] Temporary file '{name}' has been removed.")
	# 	except Exception as e:
	# 		context.logger.Log(Level.ERROR, f"[Report] Failed to remove temporary file: {e}")

# CVSS3スコアがしきい値以上でかつ(CPEのバージョンが判っている、もしくはCVE発行日時がしきい値以降である)
# 場合のCVE情報を抽出する
def filtering_cves(cveData):
	def ok(i):
		# CVEが設定された日時以降に発行されていた場合はTrue
		if i["published"] >= Config.ReportSince: return True

		# CPE内にバージョンが含まれていない場合はFalse
		splitted = i["cpe"].split(":")
		if len(splitted) < 5: return False
		if splitted[4] == "" or splitted[4] == "*": return False

		# 含まれている場合はTrue
		return True

	return [i for i in cveData
		if i["cvss3"] >= Config.ReportMinCVSS3 and ok(i)]

def mkhtml(ctx: Context, cveData, hostCpes) -> bytes:
	baseHtml = ET.fromstring("""\
<html>
	<head>
		<meta charset="UTF-8" />
		<title>lorem</title>
		<meta name="viewport" content="width=device-width, initial-scale=1" />
	</head>
	<body>
		<h1>ASM レポート</h1>
		<h2>全ホスト</h2>
		<table border="1">
			<thead>
				<tr>
					<th>CPE文字列</th>
					<th>CVE ID</th>
					<th>CVSS3</th>
					<th>発行日</th>
					<th>CVEの説明</th>
					<th>Gemini</th>
				</tr>
			</thead>
			<tbody id="allhosts">
			</tbody>
		</table>
		<h2>ホスト別</h2>
		<table border="1">
			<thead>
				<tr>
					<th>ホスト</th>
					<th>CPE文字列</th>
					<th>CVE ID</th>
					<th>CVSS3</th>
					<th>発行日</th>
					<th>CVEの説明</th>
					<th>Gemini</th>
				</tr>
			</thead>
			<tbody id="perhosts">
			</tbody>
		</table>
	</body>
</html>
""")
	allhosts = baseHtml.find("./body/table/tbody[@id='allhosts']")
	perhosts = baseHtml.find("./body/table/tbody[@id='perhosts']")
	if allhosts == None or perhosts == None: raise Exception("allhosts or perhosts is None")

	dic = dict()
	for cve in cveData:
		row = ET.Element("tr")
		cpe = ET.Element("td")
		cveId = ET.Element("td")
		cvss3 = ET.Element("td")
		published = ET.Element("td")
		cveDesc = ET.Element("td")
		extra = ET.Element("td")

		cpe.text = cve["cpe"]
		cveId.text = cve["id"]
		cveDesc.text = cve["summary"] if cve["summary"] != None else ""
		published.text = cve["published_str"]
		extra.text = cve["gemini"]

		score = cve["cvss3"]
		cvss3.text = str.format("{:.1f}", score)
		# 色付け処理がおかしくならないよう、scoreを0.0以上10.0以下に収める
		# (表内テキストでは-1と0を区別できるようにするために収める前の値を設定する)
		score = min(10.0, max(0.0, score))
		# CVSS3の色付け
		# スコアが高いほどhighの色に、低いほどlowの色に寄っていく
		high = 0xcc0000  # 赤
		low = 0xffffff   # 白
		# 背景色。RGBそれぞれ分けて計算する。分けないとおかしな結果になる
		bgColor = str.format("{:02x}{:02x}{:02x}",
			int(((high >> 16) & 0xff) * (score / 10.0)) + int(((low >> 16) & 0xff) * (1 - (score / 10.0))),
			int(((high >>  8) & 0xff) * (score / 10.0)) + int(((low >>  8) & 0xff) * (1 - (score / 10.0))),
			int(((high >>  0) & 0xff) * (score / 10.0)) + int(((low >>  0) & 0xff) * (1 - (score / 10.0)))
		)
		# 前景色
		fgColor = "#ffffff" if score >= 8.0 else "#000000"

		# CSS
		cvss3.attrib["style"] = f"background-color: #{bgColor}; color: {fgColor}; text-align: right;"

		t = (cveId, cvss3, cveDesc, published, extra)
		if cve["cpe"] in dic:
			dic[cve["cpe"]].append(t)
		else:
			dic[cve["cpe"]] = [t]

		row.append(cpe)
		row.append(cveId)
		row.append(cvss3)
		row.append(published)
		row.append(cveDesc)
		row.append(extra)
		allhosts.append(row)

	for hostCpe in hostCpes:
		for cpe in hostCpe[1]:
			if cpe not in dic: continue
			for i in dic[cpe]:
				row = ET.Element("tr")
				host = ET.Element("td")
				cpee = ET.Element("td")

				host.text = hostCpe[0]
				cpee.text = cpe

				row.append(host)
				row.append(cpee)
				for j in i:
					row.append(j)
				perhosts.append(row)

	return b"<!DOCTYPE html>\n" + ET.tostring(baseHtml, encoding="UTF-8")

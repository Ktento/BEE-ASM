#!/usr/bin/env python3
import csv
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import smtplib
from typing import Any
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

import requests

import asm.proc_db as DB
from context import Context
from log import Level

# 型エイリアス
_CveData = list[Any]
_HostCpes = dict[str, set[str]]
_HostCpePorts = dict[tuple[str, str], set[str]]

class ProcReport:
	__context: Context
	def __init__(self, context: Context) -> None:
		self.__context = context
	def review_description(self, description):
		# print(f"description: {description}")
		API_KEY = self.__context.session.server_config._gemini_api_key
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

	def create_csvs(self, cveData: _CveData, hostCpes: _HostCpes, hostCpePorts: _HostCpePorts, fAll, fPer):
		# 全ホストのCVE情報
		wa = csv.DictWriter(fAll, ["CPE", "CVEID", "CVSS3", "CVSS", "Published", "Description", "Gemini"])
		wa.writeheader()

		# ホストごとのCVE情報
		wp = csv.DictWriter(fPer, ["Host", "Ports", "CPE", "CVEID", "CVSS3", "CVSS", "Published", "Description", "Gemini"])
		wp.writeheader()

		dic = dict()
		for cve in cveData:
			d = {
				"CPE": cve["cpe"],
				"CVEID": cve["id"],
				"CVSS3": str.format("{:.1f}", cve["cvss3"]),
				"CVSS": str.format("{:.1f}", cve["cvss"]),
				"Published": cve["published_str"],
				"Description": cve["summary"],
				"Gemini": cve["gemini"],
			}
			wa.writerow(d)

			if cve["cpe"] in dic:
				dic[cve["cpe"]].append(d)
			else:
				dic[cve["cpe"]] = [d]

		for hostCpe in hostCpes.keys():
			for cpe in hostCpes[hostCpe]:
				if cpe not in dic: continue
				for i in dic[cpe]:
					i["Host"] = hostCpe
					i["Ports"] = "(Unknown)"
					if (hostCpe, cpe) in hostCpePorts:
						i["Ports"] = str.join(", ", hostCpePorts[(hostCpe, cpe)])
					wp.writerow(i)

	def send_email(self, ctx, body, attachments):
		# 送信元や宛先など
		from_email = self.__context.config.report_from
		to_email = ""
		cc_mail = str.join(",", self.__context.config.report_emails)
		mail_title = "ASMツール実行のお知らせ"
		message = body

		# MIMEオブジェクトでメールを作成
		msg = MIMEMultipart()
		msg["Subject"] = mail_title
		msg["From"] = from_email
		msg["To"] = to_email
		msg["Bcc" if self.__context.config.report_enable_bcc else "Cc"] = cc_mail

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

	def makereport(self):
		context = self.__context
		cve_data_array = context.session.result.cve_data
		host_cpes = context.session.result.host_cpes
		host_cpe_ports = context.session.result.host_cpe_ports
		context.logger.Log(Level.INFO, f"[Report] Getting CVE information...")

		# 諸条件に一致するCVE情報のみ抽出する
		filtered = self.filtering_cves(cve_data_array)
		cve_data_array = filtered["cveData"]
		for c in cve_data_array:
			c["gemini"] = "(Not permitted)"

		# Gemini有効時、抽出したものをレビューしてもらう
		if self.__context.config.report_enable_gemini:
			for c in cve_data_array[:self.__context.config.report_limit]:
				try:
					#DB利用
					if self.__context.session.enable_db:
						connection = DB.connect_to_db(context)
						if connection:
							#CVE_IDを元にDBに格納されているGeminiの説明を取得
							result=DB.select_cve_ai(connection,c["id"])
							if result:
								c["gemini"]=result
								DB.close_connection(connection)
							#接続できない　or 存在しない場合はGeminiにアクセス
							#Geminiによるレビューを受けたあとDBにその情報を登録
							else:
								#一度connectionをclose(他セッションとのトランザクション競合を避けるため)
								DB.close_connection(connection)
								connection2 = DB.connect_to_db(context)
								if connection2:
									c["gemini"] = self.review_description(c["summary"])
									columns = ["CVE_id", "CVE_description", "AI_analysis", "CPE","published"]
									cvedata=[
										(c["id"],c["summary"],c["gemini"],c["cpe"],c["published_str"])
									]
									DB.insert_sql(context,connection,"CVE",columns,cvedata)
									DB.close_connection(connection)
								else:
									context.logger.Log(Level.ERROR,f"[DB] Could not reconnect to store CVE {c['id']} after Gemini analysis.")
					else:
						c["gemini"] = self.review_description(c["summary"])
				except Exception as e:
					c["gemini"] = "(Failed)"

		extra = ""
		if len(filtered["unknownVersionFound"]) > 0:
			ss = set(filtered["unknownVersionFound"])
			since = self.__context.config.report_since.strftime("%Y年%m月%d日")
			extra = f"<p>以下のプラットフォームのバージョンを検出できませんでした。それらのCVE情報は代替として{since}以降に発行されたものを出力しています。</p><ul>"
			for sss in ss:
				extra += "<li>"
				splitted = sss.split(":")
				if len(splitted) > 3:
					extra += f"{splitted[2]} {splitted[3]}"
				elif len(splitted) > 2:
					extra += f"{splitted[2]}"
				else:
					extra += f"{sss}"
				extra += "</li>"
			extra += "</ul>"

		# HTML文書作成
		html = self.mkhtml(context, cve_data_array, host_cpes, host_cpe_ports, extra)
		try:
			with open(f"{context.savedir}/cve_report.html", "wb") as f: f.write(html)
		except Exception as e:
			context.logger.Log(Level.ERROR, f"[Report] Failed to write the HTML report to file: {e}")

		# 全ホストのCVEを格納するCSVのファイル名
		csv_filename_all = f"{context.savedir}/cve_report_all.csv"
		# ホストごとのCVEを格納するCSVのファイル名
		csv_filename_per = f"{context.savedir}/cve_report_per.csv"

		# CSVファイルの作成
		enc = self.__context.config.report_csv_encoding if self.__context.config.report_csv_encoding is not None \
			and self.__context.config.report_csv_encoding != "" else "utf-8"
		with open(csv_filename_all, mode='w', newline='', encoding=enc) as csvfile_all, \
			open(csv_filename_per, mode='w', newline='', encoding=enc) as csvfile_per:
			self.create_csvs(cve_data_array, host_cpes, host_cpe_ports, csvfile_all, csvfile_per)

		try:
			with open(csv_filename_all, mode='r', newline='', encoding=enc) as csvfile_all, \
				open(csv_filename_per, mode='r', newline='', encoding=enc) as csvfile_per:
				context.session.result.report_csv_all = csvfile_all.read()
				context.session.result.report_csv_per = csvfile_per.read()
		except Exception as e: context.logger.Log(Level.ERROR, f"[Report] Failed to store CVS results: {e}")

		# CSVを添付してEメール送信
		context.logger.Log(Level.INFO, f"[Report] Sending mail...")
		self.send_email(context, html, [csv_filename_all, csv_filename_per])
		context.session.result.report_sent = True
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
	def filtering_cves(self, cveData):
		unknownVerFound = []
		def ok(i, unknownVerFound):
			# CVEが設定された日時以降に発行されていた場合はTrue
			if i["published"] >= self.__context.config.report_since: return True

			# CPE内にバージョンが含まれていない場合はFalse
			splitted = i["cpe"].split(":")
			if len(splitted) < 5 or splitted[4] == "" or splitted[4] == "*":
				unknownVerFound.append(i["cpe"])
				return False

			# 含まれている場合はTrue
			return True

		return {
			"cveData": [i for i in cveData
				if i["cvss3"] >= self.__context.config.report_min_cvss3 and ok(i, unknownVerFound)],
			"unknownVersionFound": unknownVerFound
		}

	def mkhtml(self, ctx: Context, cveData: _CveData, hostCpes: _HostCpes, hostCpePorts: _HostCpePorts, extra_text: str) -> bytes:
		baseHtml = ET.fromstring(f"""\
	<html>
		<head>
			<meta charset="UTF-8" />
			<title>ASM report</title>
			<meta name="viewport" content="width=device-width, initial-scale=1" />
			<style>
				body {{
					background-color: white;
					color: black;
				}}
				table {{
					width: 1800px;
					border: solid 2px #1da1f2;
					border-collapse: collapse;
				}}
				tr {{
					background-color: white;
				}}
				tr:nth-child(even) {{
					background-color: #f6f6f6;
				}}
				th {{
					border-left: solid 1px white;
					border-right: solid 1px white;
					border-bottom: solid 1px #1da1f2;
					background-color: #1da1f2;
					background-image: linear-gradient(#1da1f2, #6ac0f6);
					background-image: linear-gradient(0deg, #6ac0f6 0%, #1da1f2 50%, #35aaf3 50%, #1da1f2 100%);
					text-shadow: 0px 1px 4px black;
					color: white;
				}}
				td {{
					border: solid 1px #aaa;
					padding: 2px 3px;
				}}
				h1 {{
					padding: 3px 10px;
					background-color: #6ac0f6;
					background-image: linear-gradient(#6ac0f6, white);
				}}
				h2 {{
					border-left: solid 10px #1da1f2;
					padding-left: 10px;
				}}
			</style>
		</head>
		<body>
			<h1>ASM レポート</h1>
	{extra_text}
			<p>ジャンプ: <a href="#allhostshdr">全ホスト</a> | <a href="#perhostshdr">ホスト別</a></p>
			<h2 id="allhostshdr">全ホスト</h2>
			<table border="1" cellspacing="0" cellpadding="0">
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
			<h2 id="perhostshdr">ホスト別</h2>
			<table border="1" cellspacing="0" cellpadding="0">
				<thead>
					<tr>
						<th>ホスト</th>
						<th>ポート</th>
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

		# キー: CPE文字列, 値: CVE情報のタプル
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
			bgColor = "ffffff"  # デフォルト。白
			if 9.0 <= score: bgColor = "f41907"    # 赤
			elif 7.0 <= score: bgColor = "f66e0b"  # 橙
			elif 4.0 <= score: bgColor = "fbbc04"  # 黄
			elif 0.1 <= score: bgColor = "21b803"  # 緑
			# 前景色
			fgColor = "000000"

			# CSS
			cvss3.attrib["style"] = f"background-color: #{bgColor}; color: #{fgColor}; text-align: right;"

			t = (cveId, cvss3, published, cveDesc, extra)
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

		for hostCpe in hostCpes.keys():
			for cpe in hostCpes[hostCpe]:
				if cpe not in dic: continue
				for i in dic[cpe]:
					row = ET.Element("tr")
					host = ET.Element("td")
					ports = ET.Element("td")
					cpee = ET.Element("td")

					host.text = hostCpe
					cpee.text = cpe

					ports.text = "(Unknown)"
					if (hostCpe, cpe) in hostCpePorts:
						ports.text = str.join(", ", hostCpePorts[(hostCpe, cpe)])

					row.append(host)
					row.append(ports)
					row.append(cpee)
					for j in i:
						row.append(j)
					perhosts.append(row)

		rslt: bytes = b"<!DOCTYPE html>\n" + ET.tostring(baseHtml, encoding="UTF-8") + b"\n"
		try: ctx.session.result.report_html = rslt.decode("utf-8")
		except Exception as e: ctx.logger.Log(Level.ERROR, f"[Report] Failed to store HTML result: {e}")
		return rslt

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
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from xml.dom import minidom
from datetime import datetime, timedelta
from context import Context
from log import Level
import config as Config

def get(url: str):
	# disable SSL verification
	ssl_context = ssl._create_unverified_context()
	return urllib.request.urlopen(url, context=ssl_context).read().decode("utf-8")

# cve_idとcve_titleの配列を受け取りcve_entryを完成させる関数。
def get_cve_ids(context, cve_data_array, output, cve_data):
	count = 0
	cnt = 0
	for cve in cve_data_array:
		if cnt >= Config.ReportLimit: break
		cnt += 1
		cve_entry = {
			"CVE-ID": cve["id"],
			"Title": cve["summary"],
			"Description (English)": "",
			"Gemini Review": ""
		}
		context.logger.Log(Level.INFO, f"[Report] Processing {cve['id']}...")
		output.append(f"<h2>CVE ID: {cve['id']}</h2>")
		if cve["cvss"] >= 0.0:
			output.append(f"<h3>CVSS score: {cve['cvss']}</h3>")
		if cve["cvss3"] >= 0.0:
			output.append(f"<h3>CVSS3 score: {cve['cvss3']}</h3>")

		output.append(f"<h3>Title: {cve['summary']}</h3>")

		descriptions = get_info_by_cve_id(cve["id"], cve_entry)
		count += 1

		if count % 3 == 0:
			time.sleep(15)

		cve_data.append(cve_entry)

# CVE-2002-1399
# Unknown vulnerability in cash_out and possibly other functions in PostgreSQL 7.2.1 and earlier, and possibly later versions before 7.2.3, with unknown impact, based on an invalid integer input which is processed as a different data type, as demonstrated using cash_out(2).

def get_info_by_cve_id(cve_id: str, cve_entry):
	max_retries = 5
	retry_delay = 5

	try:
		url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?cveId={cve_id}"
		response = get(url=url)
		data = json.loads(response)

		if "vulnerabilities" in data and data["vulnerabilities"]:
			en_descriptions = []
			for vulnerability in data["vulnerabilities"]:
				cve = vulnerability.get("cve", {})
				descriptions = cve.get("descriptions", [])
				for description in descriptions:
					if description.get("lang") == "en":
						en_descriptions.append(description.get("value"))

			if en_descriptions:
				description = en_descriptions[0]  # 最初の説明文を使用
				cve_entry["Description (English)"] = description
				review = review_description(description)
				if review:
					cve_entry["Gemini Review"] = review
				return en_descriptions

		# print(f"No English description found for {cve_id}")
		return None
	except Exception as e:
		# print(f"Error getting info for {cve_id}: {e}")
		return None

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
		# print(f"failed. http status code: {response.status_code}")
		# print("preview:", response.text)

def create_csv(cve_data, filename):
	if not cve_data:
		# print("No CVE data to write to CSV")
		return False

	try:
		with open(filename, mode='w', newline='', encoding='utf-8') as csvfile:
			fieldnames = ["CVE-ID", "Title", "Description (English)", "Gemini Review"]
			writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

			# ヘッダーを書き込む
			writer.writeheader()

			# すべてのエントリーを書き込む
			for entry in cve_data:
				writer.writerow(entry)

			# ファイル作成完了のメッセージは1回だけ表示
			# print(f"CSV file '{filename}' created successfully with {len(cve_data)} entries.")
			return True

	except Exception as e:
		# print(f"Failed to create CSV file: {e}")
		return False


def send_email(ctx, output, attachment_path):
	from_email = Config.ReportFrom
	to_email = ''
	cc_mail = str.join(",", Config.ReportEmails)
	mail_title = 'ASMツール実行のお知らせ'
	message = str.join("", output)

	#  MIMEオブジェクトでメールを作成
	msg = MIMEMultipart()
	msg['Subject'] = mail_title
	msg['From'] = from_email
	msg['To'] = to_email
	msg['Bcc' if Config.ReportEnableBCC else "Cc"] = cc_mail

	msg.attach(MIMEText(message, 'html'))

	if Config.ReportLimit > 0:
		try:
			with open(attachment_path, "rb") as attachment:
				part = MIMEBase("application", "octet-stream")
				part.set_payload(attachment.read())
			encoders.encode_base64(part)
			part.add_header(
				"Content-Disposition",
				f"attachment; filename={os.path.basename(attachment_path)}",
			)
			msg.attach(part)
			# print(f"Attached file '{attachment_path}' to the email.")
		except Exception as e:
			ctx.logger.Log(Level.ERROR, f"[Report] Failed to attach file: {e}")

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

def makereport(context: Context, cve_data_array):
	context.logger.Log(Level.INFO, f"[Report] Getting CVE information...")
	output = ["<h1>ASMツール実行のお知らせ</h1>"]
	cve_data = []

	# Step 1: Collect the CVE Data
	get_cve_ids(context, cve_data_array[:31], output=output, cve_data=cve_data)
	context.logger.Log(Level.INFO, f"[Report] Getting CVE info finished.")

	# Step 2: Create CSV File
	context.logger.Log(Level.INFO, f"[Report] Generating report...")
	current_date = datetime.now().strftime("%Y%m%d")
	csv_filename = f"{context.savedir}/cve_report_{current_date}.csv"
	create_csv(cve_data, csv_filename)
	context.logger.Log(Level.INFO, f"[Report] Generating report finished.")

	# Step 3: Send Email with Attachment
	context.logger.Log(Level.INFO, f"[Report] Sending mail...")
	send_email(context, output, attachment_path=csv_filename)
	context.logger.Log(Level.INFO, f"[Report] Mail sent.")

	# Optional: Remove the CSV file after sending the email
	# try:
	# 	os.remove(csv_filename)
	# 	context.logger.Log(Level.INFO, f"[Report] Temporary file '{csv_filename}' has been removed.")
	# except Exception as e:
	# 	context.logger.Log(Level.ERROR, f"[Report] Failed to remove temporary file: {e}")

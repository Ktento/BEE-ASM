#!/usr/bin/env python3
import os, sys, time, subprocess
import xml.etree.ElementTree as ET
import config as Config
from context import Context
import proc_nmap as Nmap
import proc_ddg as DDG  # DDG ... DuckDuckGo
import proc_subfinder as Subfinder
import proc_report as Report
import proc_cve as CVE
from log import Logger, Level
import json

if __name__ == "__main__":
	# 結果出力先の作成
	# 結果は カレントディレクトリー/result_<整数のUNIX時刻>/
	# に保存される
	time = int(time.time())
	resultdir = f"./result_{time}"
	os.mkdir(resultdir)
	logger = Logger(f"{resultdir}/log.txt")
	ctx = Context(logger, resultdir, Config.TargetHosts)
	# 簡略化用
	Log = logger.Log

	def end():
		Log(Level.INFO, f"===== APPLICATION FINISHED (PID: {os.getpid()}) =====")

	# アプリケーションが起動したこと、および自身のPID そしてログ出力先をログに残す
	Log(Level.INFO, f"===== APPLICATION STARTED (PID: {os.getpid()}) =====")
	Log(Level.INFO, f"Current directory: {os.getcwd()}")
	Log(Level.INFO, f"Writing logs to: {logger.filename}")

	# いわゆる免責事項。「このツールは無保証で提供されます。発生したいかなる損害もあなたの責任となります。」
	Log(Level.INFO, "DISCLAIMER: This tool is provided without warranty. Any damage caused is your own responsibility.")

	# 有効になっている検査機能もログに残す
	Log(Level.INFO, "subfinder: " + ("Enabled" if Config.EnableSubfinder else "Disabled"))
	Log(Level.INFO, "Reporting feature: " + ("Enabled" if Config.EnableReporting else "Disabled"))
	Log(Level.INFO, "Nmap: " + ("Enabled" if Config.EnableNmap else "Disabled"))
	Log(Level.INFO, "Web search feature (DDG): " + ("Enabled" if Config.SearchWeb else "Disabled"))
	Log(Level.INFO, "CVE search feature: " + ("Enabled" if Config.SearchCVE and Config.EnableNmap else "Disabled"))

	if not Config.EnableNmap and Config.SearchCVE:
		Log(Level.WARN, "CVE search feature disabled due to Nmap is disabled in config.")

	# 脆弱性診断ツール(VAT)を有効にする場合、決意を問う
	# というのもASMツールの範疇を超えているため
	ensured = Config.RepeatAfterMeIAmSureToRunTheVAT == "IAmSureToRunTheVAT"
	Log(Level.INFO, "Execute the vulnerability assessment tool (VAT): " + ("Enabled" if Config.EnableVAT and ensured else ("Not ensured" if Config.EnableVAT and not ensured else "Disabled")))
	if Config.EnableVAT and not ensured:
		Log(Level.FATAL, "To enable VAT, you need to be sure what you are going to do.")
		Log(Level.INFO, 'If you REALLY want to enable VAT, set the config "RepeatAfterMeIAmSureToRunTheVAT" to "IAmSureToRunTheVAT". Otherwise, set "EnableVAT" to False.')
		Log(Level.INFO, 'Exiting.')
		# 決意が足りなかったら終了
		# 早期に終了することで早めに修正できるようにしておく
		end()
		sys.exit(1)

	# 検査対象、および検査対象外のホストもログに残す
	Log(Level.INFO, "Target hosts: " + str.join(", ", Config.TargetHosts))
	Log(Level.INFO, "Excluded hosts (subfinder, Nmap): " + str.join(", ", Config.ExcludeHosts))

	# subfinder
	if Config.EnableSubfinder:
		try:
			# スキャン
			add_domains = Subfinder.ProcSubfinder(ctx)
			ctx.hosts += add_domains
		except Exception as e:
			Log(Level.ERROR, f"[subfinder] subfinder failed: {e}")

	Log(Level.INFO, f"New target hosts: {ctx.hosts}")

	# Nmap
	# 後の報告のためにCVEデータを格納する
	cveData = []
	if Config.EnableNmap:
		try:
			# スキャン
			nm = Nmap.ProcNmap(ctx)

			# CVE検索機能が有効なら検索する
			if Config.SearchCVE:
				# NmapはCPE文字列まで返してくれるのでそれを使う
				cpes = set()

				# python-nmap経由でCPE文字列を列挙する
				# for host in nm.all_hosts():
				# 	for proto in nm[host].all_protocols():
				# 		for port in nm[host][proto].keys():
				# 			if "cpe" in nm[host][proto][port]:
				# 				cpes.add(nm[host][proto][port]["cpe"])
				# ただし、あるサービスに2つ以上のCPE文字列があると1つのみ返される
				# そのため、代わりにNmapのXML出力からCPE文字列を取得する

				# Nmap XMLから列挙する
				elm = ET.fromstring(nm.get_nmap_last_output())
				xmlCpes = elm.findall("./host/ports/port/service/cpe")
				for i in xmlCpes:
					cpes.add(i.text)

				# 空の文字列が入る場合があるので取り除く
				cpes.discard("")
				# 少なくとも1つCPEがあれば検索する
				if len(cpes) > 0:
					try:
						cveData = CVE.ProcCVE(ctx, cpes)
						Log(Level.INFO, f"[CVE] Found {len(cveData)} CVE(s)")
					except Exception as e:
						Log(Level.ERROR, f"[CVE] Searching CVE failed: {e}")
		except Exception as e:
			Log(Level.ERROR, f"[Nmap] Nmap failed: {e}")

	# Web検索
	if Config.SearchWeb:
		try:
			# 検索
			DDG.ProcDDG(ctx)
		except Exception as e:
			Log(Level.ERROR, f"[DDG] Searching failed: {e}")

	# VATの起動
	if Config.EnableVAT and ensured:
		try:
			Log(Level.INFO, "[VAT] Launching the VAT...")
			# 起動
			vatResult = subprocess.run([Config.VATPath], capture_output=True)
			Log(Level.INFO, "[VAT] VAT finished.")
			Log(Level.INFO, f"[VAT] VAT stdout:\n{vatResult.stdout.decode('utf-8', 'replace')}")
			Log(Level.INFO, f"[VAT] VAT stderr:\n{vatResult.stderr.decode('utf-8', 'replace')}")
			Log(Level.INFO, f"[VAT] VAT return code: {vatResult.returncode}")
			with open(f"{resultdir}/vat_stdout.txt", "wb") as o, open(f"{resultdir}/vat_stderr.txt", "wb") as e:
				o.write(vatResult.stdout)
				e.write(vatResult.stderr)
		except Exception as e:
			Log(Level.ERROR, f"[VAT] VAT failed: {e}")

	# Eメールでのレポート
	if Config.EnableReporting:
		try:
			# CVE情報はCVSS3スコアの昇順でソートされているためリバースする
			# これにより処理件数を制限した場合でもCVSS3スコアの高い方が優先されてレポートされる
			cveData.reverse()
			# レポートする
			Report.makereport(ctx, cveData)
		except Exception as e:
			Log(Level.ERROR, f"[Report] Report failed: {e}")

	end()

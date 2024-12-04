#!/usr/bin/env python3

if __name__ == "__main__":
	pass

# #!/usr/bin/env python3
# import os, sys, time, subprocess
# import xml.etree.ElementTree as ET
# import config as Config
# from context import Context
# import proc_nmap as Nmap
# import proc_ddg as DDG  # DDG ... DuckDuckGo
# import proc_subfinder as Subfinder
# import proc_report as Report
# import proc_cve as CVE
# from log import Logger, Level
# import json

# if __name__ == "__main__":
# 	# 結果出力先の作成
# 	# 結果は カレントディレクトリー/result_<整数のUNIX時刻>/
# 	# に保存される
# 	time = int(time.time())
# 	resultdir = f"./result_{time}"
# 	os.mkdir(resultdir)
# 	logger = Logger(f"{resultdir}/log.txt")
# 	ctx = Context(logger, resultdir, Config.TargetHosts)
# 	# 簡略化用
# 	Log = logger.Log

# 	def end():
# 		Log(Level.INFO, f"===== APPLICATION FINISHED (PID: {os.getpid()}) =====")

# 	# アプリケーションが起動したこと、および自身のPID そしてログ出力先をログに残す
# 	Log(Level.INFO, f"===== APPLICATION STARTED (PID: {os.getpid()}) =====")
# 	Log(Level.INFO, f"Current directory: {os.getcwd()}")
# 	Log(Level.INFO, f"Writing logs to: {logger.filename}")

# 	# いわゆる免責事項。「このツールは無保証で提供されます。発生したいかなる損害もあなたの責任となります。」
# 	Log(Level.INFO, "DISCLAIMER: This tool is provided without warranty. Any damage caused is your own responsibility.")

# 	# 有効になっている検査機能もログに残す
# 	Log(Level.INFO, "subfinder: " + ("Enabled" if Config.EnableSubfinder else "Disabled"))
# 	Log(Level.INFO, "Reporting feature: " + ("Enabled" if Config.EnableReporting else "Disabled"))
# 	Log(Level.INFO, "Nmap: " + ("Enabled" if Config.EnableNmap else "Disabled"))
# 	Log(Level.INFO, "Web search feature (DDG): " + ("Enabled" if Config.SearchWeb else "Disabled"))
# 	Log(Level.INFO, "CVE search feature: " + ("Enabled" if Config.SearchCVE and Config.EnableNmap else "Disabled"))

# 	if not Config.EnableNmap and Config.SearchCVE:
# 		Log(Level.WARN, "CVE search feature disabled due to Nmap is disabled in config.")

# 	# 検査対象、および検査対象外のホストもログに残す
# 	Log(Level.INFO, "Target hosts: " + str.join(", ", Config.TargetHosts))
# 	Log(Level.INFO, "Excluded hosts (subfinder, Nmap): " + str.join(", ", Config.ExcludeHosts))

# 	# subfinder
# 	if Config.EnableSubfinder:
# 		try:
# 			# スキャン
# 			add_domains = Subfinder.ProcSubfinder(ctx)
# 			ctx.hosts += add_domains
# 		except Exception as e:
# 			Log(Level.ERROR, f"[subfinder] subfinder failed: {e}")

# 	Log(Level.INFO, f"New target hosts: {ctx.hosts}")

# 	# Nmap

# 	# 後の報告のためにCVEデータを格納する
# 	cveData = []

# 	# ホストとそのホストに対応するCPE文字列の組
# 	# [
# 	#   ("ホスト0", {"CPE文字列0", "CPE文字列1", ...}),
# 	#   ("ホスト1", {"CPE文字列0", "CPE文字列1", ...}), ...
# 	# ]
# 	# のような形式になる
# 	hostCpes = []

# 	# ホストとCPE文字列に対応するプロコトル名とポート番号
# 	# 一つのサービスに複数のポートが割り当てられていることもあるためこうする
# 	# [
# 	#   {"host": "ホスト0", "cpe": "CPE文字列0", "ports": ["プロコトル名0/ポート番号0", "プロコトル名1/ポート番号1", ...]},
# 	#   {"host": "ホスト1", "cpe": "CPE文字列1", "ports": ["プロコトル名0/ポート番号0", "プロコトル名1/ポート番号1", ...]}, ...
# 	# ]
# 	# のような形式になる
# 	hostCpePorts = []

# 	if Config.EnableNmap:
# 		try:
# 			# スキャン
# 			nm = Nmap.ProcNmap(ctx)

# 			# CVE検索機能が有効なら検索する
# 			if Config.SearchCVE:
# 				# NmapはCPE文字列まで返してくれるのでそれを使う
# 				cpes = set()

# 				# python-nmap経由でCPE文字列を列挙する場合以下のようにすれば良い:
# 				# for host in nm.all_hosts():
# 				# 	for proto in nm[host].all_protocols():
# 				# 		for port in nm[host][proto].keys():
# 				# 			if "cpe" in nm[host][proto][port]:
# 				# 				cpes.add(nm[host][proto][port]["cpe"])
# 				# ただし、あるサービスに2つ以上のCPE文字列があると1つのみ返される
# 				# そのため、ここでは代わりにNmapのXML出力からCPE文字列を取得することにする

# 				# NmapのCPE文字列を修正
# 				def fixcpe(input):
# 					try:
# 						fixes = {
# 							"cpe:/a:microsoft:iis:10.0": "cpe:/a:microsoft:internet_information_services:10.0",
# 						}
# 						return fixes[input] if input in fixes else input
# 					except Exception:
# 						return input

# 				# Nmapが出力したXMLドキュメントから列挙する
# 				elm = ET.fromstring(nm.get_nmap_last_output())
# 				xmlCpes = elm.findall("./host/ports/port/service/cpe")
# 				for i in xmlCpes:
# 					i.text = fixcpe(i.text)
# 					cpes.add(i.text)

# 				for host in elm.findall("./host"):
# 					# ユーザー入力のホスト名があればそれを使う
# 					hostnameUser = host.find("./hostnames/hostname[@type='user']")
# 					if hostnameUser is not None: hostnameUser = hostnameUser.attrib["name"]
# 					# 無ければIPアドレスを使う
# 					hostIp = host.find("./address")
# 					if hostIp is not None: hostIp = hostIp.attrib["addr"]
# 					# それも無ければ不明として扱う
# 					theName = hostnameUser if hostnameUser is not None else hostIp if hostIp is not None else "<hostname/address unknown>"

# 					xmlPorts = host.findall("./ports/port")
# 					for xmlPort in xmlPorts:
# 						p = f'{xmlPort.attrib["protocol"]}/{xmlPort.attrib["portid"]}'

# 						xmlCpes = xmlPort.findall("./service/cpe")
# 						# まとめる
# 						s = set(map(lambda i:i.text, xmlCpes))
# 						s.discard("")
# 						hostCpes.append((theName, s))

# 						for ss in s:
# 							found = False
# 							for hostCpePort in hostCpePorts:
# 								if hostCpePort["host"] == theName and hostCpePort["cpe"] == ss:
# 									hostCpePort["ports"].append(p)
# 									found = True
# 									break
# 							if not found:
# 								hostCpePorts.append({"host": theName, "cpe": ss, "ports": [p]})

# 				# 空の文字列が入る場合があるので取り除く
# 				cpes.discard("")
# 				cveData = []
# 				try:
# 					cveData = CVE.ProcCVE(ctx, cpes)
# 					Log(Level.INFO, f"[CVE] Found {len(cveData)} CVE(s)")
# 				except Exception as e:
# 					Log(Level.ERROR, f"[CVE] Searching CVE failed: {e}")
# 		except Exception as e:
# 			Log(Level.ERROR, f"[Nmap] Nmap failed: {e}")

# 	# Web検索
# 	if Config.SearchWeb:
# 		try:
# 			# 検索
# 			DDG.ProcDDG(ctx)
# 		except Exception as e:
# 			Log(Level.ERROR, f"[DDG] Searching failed: {e}")

# 	# Eメールでのレポート
# 	if Config.EnableReporting:
# 		try:
# 			# CVE情報はCVSS3スコアの昇順でソートされているためリバースする
# 			# これにより処理件数を制限した場合でもCVSS3スコアの高い方が優先されてレポートされる
# 			cveData.reverse()
# 			# レポートする
# 			Report.makereport(ctx, cveData, hostCpes, hostCpePorts)
# 		except Exception as e:
# 			Log(Level.ERROR, f"[Report] Report failed: {e}")

# 	end()

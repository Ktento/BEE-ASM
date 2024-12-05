#!/usr/bin/env python3
from fastapi import FastAPI, BackgroundTasks
import os, sys, time, subprocess
import xml.etree.ElementTree as ET
from context import Context
import asm.proc_nmap as Nmap
import asm.proc_ddg as DDG  # DDG ... DuckDuckGo
import asm.proc_subfinder as Subfinder
import asm.proc_report as Report
import asm.proc_cve as CVE
from log import Logger, Level
import json
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from pydantic import BaseModel
from typing import Any, List
from fastapi.responses import JSONResponse
from session import Session
from time import sleep

class Asm:
	def __init__(self, session: Session):
		logger = session.logger
		ctx = Context(logger, str(session.workdir), session.config.target_hosts, session.config, session)
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
		Log(Level.INFO, "subfinder: "                + ("Enabled" if session.config.enable_subfinder                          else "Disabled"))
		Log(Level.INFO, "Reporting feature: "        + ("Enabled" if session.config.enable_reporting                          else "Disabled"))
		Log(Level.INFO, "Nmap: "                     + ("Enabled" if session.config.enable_nmap                               else "Disabled"))
		Log(Level.INFO, "Web search feature (DDG): " + ("Enabled" if session.config.search_web                                else "Disabled"))
		Log(Level.INFO, "CVE search feature: "       + ("Enabled" if session.config.search_cve and session.config.enable_nmap else "Disabled"))

		if not session.config.enable_nmap and session.config.search_cve:
			Log(Level.WARN, "CVE search feature disabled due to Nmap is disabled in config.")

		assert session.progress is not None

		if session.config.enable_subfinder                         : session.progress.task_progresses["subfinder"] = 0.0
		if session.config.enable_reporting                         : session.progress.task_progresses["reporting"] = 0.0
		if session.config.enable_nmap                              : session.progress.task_progresses["nmap"] = 0.0
		if session.config.search_web                               : session.progress.task_progresses["websearch"] = 0.0
		if session.config.search_cve and session.config.enable_nmap: session.progress.task_progresses["cve"] = 0.0

		# 検査対象、および検査対象外のホストもログに残す
		Log(Level.INFO, "Target hosts: " + str.join(", ", session.config.target_hosts))
		Log(Level.INFO, "Excluded hosts (subfinder, Nmap): " + str.join(", ", session.config.exclude_hosts))

		# subfinder
		if session.config.enable_subfinder:
			try:
				# スキャン
				add_domains = Subfinder.ProcSubfinder(ctx)
				ctx.hosts += add_domains
			except Exception as e:
				Log(Level.ERROR, f"[subfinder] subfinder failed: {e}")
			finally:
				session.progress.task_progresses["subfinder"] = 1.0

		Log(Level.INFO, f"New target hosts: {ctx.hosts}")

		# Nmap

		# 後の報告のためにCVEデータを格納する
		cveData = []

		# ホストとそのホストに対応するCPE文字列の組
		# [
		#   ("ホスト0", {"CPE文字列0", "CPE文字列1", ...}),
		#   ("ホスト1", {"CPE文字列0", "CPE文字列1", ...}), ...
		# ]
		# のような形式になる
		hostCpes = []

		# ホストとCPE文字列に対応するプロコトル名とポート番号
		# 一つのサービスに複数のポートが割り当てられていることもあるためこうする
		# [
		#   {"host": "ホスト0", "cpe": "CPE文字列0", "ports": ["プロコトル名0/ポート番号0", "プロコトル名1/ポート番号1", ...]},
		#   {"host": "ホスト1", "cpe": "CPE文字列1", "ports": ["プロコトル名0/ポート番号0", "プロコトル名1/ポート番号1", ...]}, ...
		# ]
		# のような形式になる
		hostCpePorts = []

		if session.config.enable_nmap:
			try:
				# スキャン
				nm = Nmap.ProcNmap(ctx)
				session.progress.task_progresses["nmap"] = 1.0

				# CVE検索機能が有効なら検索する
				if session.config.search_cve:
					# NmapはCPE文字列まで返してくれるのでそれを使う
					cpes = set()

					# python-nmap経由でCPE文字列を列挙する場合以下のようにすれば良い:
					# for host in nm.all_hosts():
					# 	for proto in nm[host].all_protocols():
					# 		for port in nm[host][proto].keys():
					# 			if "cpe" in nm[host][proto][port]:
					# 				cpes.add(nm[host][proto][port]["cpe"])
					# ただし、あるサービスに2つ以上のCPE文字列があると1つのみ返される
					# そのため、ここでは代わりにNmapのXML出力からCPE文字列を取得することにする

					# NmapのCPE文字列を修正
					def fixcpe(input):
						try:
							fixes = {
								"cpe:/a:microsoft:iis:10.0": "cpe:/a:microsoft:internet_information_services:10.0",
							}
							return fixes[input] if input in fixes else input
						except Exception:
							return input

					# Nmapが出力したXMLドキュメントから列挙する
					elm = ET.fromstring(nm.get_nmap_last_output())
					xmlCpes = elm.findall("./host/ports/port/service/cpe")
					for i in xmlCpes:
						i.text = fixcpe(i.text)
						cpes.add(i.text)

					for host in elm.findall("./host"):
						# ユーザー入力のホスト名があればそれを使う
						hostnameUser = host.find("./hostnames/hostname[@type='user']")
						if hostnameUser is not None: hostnameUser = hostnameUser.attrib["name"]
						# 無ければIPアドレスを使う
						hostIp = host.find("./address")
						if hostIp is not None: hostIp = hostIp.attrib["addr"]
						# それも無ければ不明として扱う
						theName = hostnameUser if hostnameUser is not None else hostIp if hostIp is not None else "<hostname/address unknown>"

						xmlPorts = host.findall("./ports/port")
						for xmlPort in xmlPorts:
							p = f'{xmlPort.attrib["protocol"]}/{xmlPort.attrib["portid"]}'

							xmlCpes = xmlPort.findall("./service/cpe")
							# まとめる
							s = set(map(lambda i:i.text, xmlCpes))
							s.discard("")
							hostCpes.append((theName, s))

							for ss in s:
								found = False
								for hostCpePort in hostCpePorts:
									if hostCpePort["host"] == theName and hostCpePort["cpe"] == ss:
										hostCpePort["ports"].append(p)
										found = True
										break
								if not found:
									hostCpePorts.append({"host": theName, "cpe": ss, "ports": [p]})

					# 空の文字列が入る場合があるので取り除く
					cpes.discard("")
					cveData = []
					try:
						cveData = CVE.ProcCVE(ctx, cpes)
						Log(Level.INFO, f"[CVE] Found {len(cveData)} CVE(s)")
					except Exception as e:
						Log(Level.ERROR, f"[CVE] Searching CVE failed: {e}")
					finally:
						session.progress.task_progresses["cve"] = 1.0
			except Exception as e:
				Log(Level.ERROR, f"[Nmap] Nmap failed: {e}")
			finally:
				session.progress.task_progresses["nmap"] = 1.0

		# Web検索
		if session.config.search_web:
			try:
				# 検索
				DDG.ProcDDG(ctx)
			except Exception as e:
				Log(Level.ERROR, f"[DDG] Searching failed: {e}")
			finally:
				session.progress.task_progresses["websearch"] = 1.0

		# Eメールでのレポート
		if session.config.enable_reporting:
			try:
				# CVE情報はCVSS3スコアの昇順でソートされているためリバースする
				# これにより処理件数を制限した場合でもCVSS3スコアの高い方が優先されてレポートされる
				cveData.reverse()
				# レポートする
				Report.ProcReport(ctx).makereport(ctx, cveData, hostCpes, hostCpePorts)
			except Exception as e:
				Log(Level.ERROR, f"[Report] Report failed: {e}")
			finally:
				session.progress.task_progresses["reporting"] = 1.0

		session.progress.task_progresses["asm"] = 1.0
		end()

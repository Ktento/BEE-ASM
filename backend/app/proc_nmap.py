#!/usr/bin/env python3
# Pythonパッケージ「python-nmap」との競合を防ぐためファイル名をproc_nmap.pyとしている
from nmap import PortScanner
import config as Config
from context import Context
from log import Level

def ProcNmap(context: Context) -> PortScanner:
	context.logger.Log(Level.INFO, f"[Nmap] Scanning with Nmap...")
	nm = PortScanner()
	extraArgs = ["-sV"]
	if len(Config.ExcludeHosts) > 0:
		extraArgs.append("--exclude")
		extraArgs.append(str.join(",", Config.ExcludeHosts))
	extraArgs += Config.NmapExtraArgs

	try:
		# Nmap XML出力モード(-oX)の結果をそのまま書き込む
		fname = f"{context.savedir}/nmap_result.xml"
		with open(fname, "wb") as f:
			# argumentsはstr型のみ渡せるためjoinする
			nm.scan(str.join(" ", context.hosts), arguments=str.join(" ", extraArgs))
			# 実際にget_nmap_last_output()を呼ぶとbytesが返ってくるが
			# Pyrightでは戻り値の型がstrだと認識されるため、また実際にstrを返しそうなコードがpython-nmap内にあるため
			# bytesの場合とstrの場合に対応する
			out = nm.get_nmap_last_output()
			f.write(out if type(out) is bytes else out.encode())
		context.logger.Log(Level.INFO, f"[Nmap] Wrote scan result to {fname}.")
	except Exception as e:
		context.logger.Log(Level.ERROR, f"[Nmap] Scan failed: {e}")

	context.logger.Log(Level.INFO, f'[Nmap] Scan finished.')
	return nm

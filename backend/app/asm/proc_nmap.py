#!/usr/bin/env python3
import subprocess

from context import Context
from log import Level

def ProcNmap(context: Context) -> str:
	xml = ""
	try:
		context.logger.Log(Level.INFO, f"[Nmap] Scanning with Nmap...")
		extraArgs = ["nmap", "-sV", "-oX", "-", *context.config.target_hosts]
		if len(context.config.exclude_hosts) > 0:
			extraArgs.append("--exclude")
			extraArgs.append(str.join(",", context.config.exclude_hosts))
		extraArgs += context.config.nmap_extra_args
		result = subprocess.run(extraArgs, capture_output=True, text=True, check=False, shell=False)
		xml = result.stdout

		# Nmap XML出力モード(-oX)の結果をそのまま書き込む
		fname = f"{context.savedir}/nmap_result.xml"
		fname_err = f"{context.savedir}/nmap_result_stderr.txt"
		with open(fname, "w") as f, open(fname_err, "w") as g:
			f.write(result.stdout)
			g.write(result.stderr)
		context.logger.Log(Level.INFO, f"[Nmap] Wrote scan result to {context.savedir}/nmap_result(.xml|_stderr.txt).")
	except Exception as e:
		context.logger.Log(Level.ERROR, f"[Nmap] Scan failed: {e}")

	context.logger.Log(Level.INFO, f'[Nmap] Scan finished.')
	return xml

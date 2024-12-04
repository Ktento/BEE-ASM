#!/usr/bin/env python3
import subprocess
import config as Config
from context import Context
from log import Level

def ProcSubfinder(context: Context) -> list:
	context.logger.Log(Level.INFO, f"[subfinder] Scanning with subfinder...")
	# 検出できたドメインを保存するリスト
	domains = []
	ips = []

	try:
		# subfinderを実行するコマンドを構築
		# 検査対象のドメイン、検査対象外のドメインをコマンド実行できるように文字結合
		tgtStr = str.join(",", Config.TargetHosts)
		exlStr = str.join(",", Config.ExcludeHosts)

		command = ['subfinder', '-d', tgtStr, '-ip', '-nW', '-t', '100']
		# 検査対象外のホストがある場合-fオプションを追加
		if len(Config.ExcludeHosts) > 0:
			command += ['-f', exlStr]

		# subprocessを使ってsubfinderを実行
		result = subprocess.run(command, capture_output=True, text=True, check=True)
		# 正常に結果が得られた場合、stdoutからドメインとIPアドレスを抽出
		if result.returncode == 0:
			# stdoutには「ドメイン名,IPアドレス」形式で出力される
			output_lines = result.stdout.strip().split("\n")
			for line in output_lines:
				# 空行なら飛ばす。これがないとサブドメインが
				# 見つからなかった場合にこれがないとエラーになる
				if line == "": continue
				domain, ip, _ = line.split(",", 2)  # ドメイン名とIPアドレスを取得
				domains.append(domain)
				ips.append(ip)

		context.logger.Log(Level.INFO, f'[subfinder] Scan finished.')
		return domains
	except subprocess.CalledProcessError as e:
		context.logger.Log(Level.ERROR, f"[subfinder] Scan failed: {e}")
		return []

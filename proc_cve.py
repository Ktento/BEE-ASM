#!/usr/bin/env python3
import config as Config
from context import Context
from log import Level
import urllib.request
import json
from datetime import datetime

# メモ: jq '. | sort_by(.cvss3) | map({(.id|tostring): (.cvss3)}) | add' FILE.json
#       jq '[. | sort_by(.cvss3)[] | {"\(.id)": (.cvss3)}] | add' FILE.json

def ProcCVE(context: Context, cpes: set) -> list:
	"""CVEに関する処理です。
	戻り値はCVSS3の昇順でソートされたものです。
	CVSS, CVSS3のスコアがないものはそれぞれ代わりに-1.0をスコアとしています。"""

	# CVE IDs
	result = []
	context.logger.Log(Level.INFO, f"[CVE] Searching CVEs with CIRCL CVE-Search API...")
	for cpe in cpes:
		# リクエスト発行先のURL
		url = f"{Config.CVEAPIBase}/cvefor/{cpe}"

		# ファイル名用にCPE文字列から置き換える対象の文字列
		# 後の処理で"cve_<置換済みのCPE文字列>.json"に保存する
		# 例: CPE文字列が"cpe:/a:lorem:ipsum"なら
		#     出力ファイル名は"cve_cpe@@a@lorem@ipsum.json"となる
		# ext4ならNULL文字'\0'とスラッシュ'/'以外であればファイル名に使えるが
		# Windowsだといくつかの記号や予約済みファイル名(AUXやNULなど)は使用できない
		# 移植性を高めるためここでは一部記号を'@'に置換する
		r = [":", "/", "\\", '"', "*", "?", "<", ">", "|"]
		escaped = cpe
		for i in r:
			escaped = escaped.replace(i, "@")

		# 出力先のファイルパス
		output = f"{context.savedir}/cve_{escaped}.json"
		try:
			context.logger.Log(Level.INFO, f'[CVE] Searching CVEs for CPE "{cpe}"...')

			# ダウンロードと保存
			with urllib.request.urlopen(url) as r, open(output, "w") as f:
				b = r.read()
				js = json.loads(b)
				# CVSS3スコアで昇順ソートしてファイルへ保存
				# スコアがない場合、-1.0を代替にしてソートする
				sortedStr = sorted(js, key=lambda x:x["cvss3"] if "cvss3" in x else -1.0)
				f.write(json.dumps(sortedStr, ensure_ascii=False, indent=None))

			# 結果のJSONからまとめる
			for v in js:
				if "id" not in v: continue

				# 発行日時。デフォルトで1970-01-01 00:00:00 (Unixエポック)
				pubdate = datetime(1970, 1, 1, 0, 0, 0)
				if "Published" in v:
					try:
						pubdate = datetime.fromisoformat(v["Published"])
					except: pass
				result.append({
					"cpe": cpe,  # 入力のCPE文字列。どの入力に対する結果であるかを区別できるようにするため
					"id": v["id"],  # CVE ID ("CVE-YYYY-NNNN+")
					"published": pubdate,  # 発行日時
					"cvss": v["cvss"] if "cvss" in v else -1.0,
					"cvss3": v["cvss3"] if "cvss3" in v else -1.0,
					"summary": v["summary"] if "summary" in v else None
				})

		except Exception as e:
			context.logger.Log(Level.ERROR, f'[CVE] Search CVEs for CPE "{cpe}" failed: {e}')
	context.logger.Log(Level.INFO, f"[CVE] Search finished.")

	# CVSS3スコアでソートしたものを返す
	# 上でもソートしているが、CPE個別でのソートとなっているため
	# ここで全体をソートし直す
	return sorted(result, key=lambda x:x["cvss3"])

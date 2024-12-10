#!/usr/bin/env python3
# DDG ... DuckDuckGo
import json

from duckduckgo_search import DDGS

from context import Context
from log import Level

def ProcDDG(context: Context) -> None:
	# ターゲットとなるホストすべてに site: を頭に付ける
	# 例えば["example.com", "example.org"]がターゲットなら
	# "site:example.com OR site:example.org"となる

	# site:クエリ配列
	tgt = []
	for a in context.hosts:
		tgt.append(f"site:{a}")

	# さっき作ったsite:クエリと設定のクエリを合成する
	query = f"{str.join(' OR ', tgt)} {context.config.web_query}"

	# 実際に検索する
	context.logger.Log(Level.INFO, f'[DDG] Searching "{query}" on DuckDuckGo...')
	try:
		fname = f"{context.savedir}/web_search_result.json"
		with open(fname, "w") as f:
			results = None
			backend = context.config.web_backend if context.config.web_backend is not None and context.config.web_backend != "" else "html"

			results = DDGS().text(query, max_results=context.config.web_max_results, backend=backend, region=context.config.web_region)

			context.logger.Log(Level.FATAL, f"RSLTS: {results}")
			j = json.dumps(results, ensure_ascii=False, indent=None)
			try: context.session.result.web = j
			except Exception as e: context.logger.Log(Level.ERROR, f"[DDG] Failed to store result: {e}")
			f.write(j)
		context.logger.Log(Level.INFO, f"[DDG] Wrote search result to {fname}.")
	except Exception as e:
		context.logger.Log(Level.ERROR, f"[DDG] Search failed: {e}")
	context.logger.Log(Level.INFO, "[DDG] Search finished.")

#!/usr/bin/env python3
from datetime import datetime

from pydantic import BaseModel, Field

# リクエストボディ用モデル
class ConfigModel(BaseModel):
	"""ユーザー(クライアント)が変更可能な設定

	`target_hosts`をはじめとする「ホスト名を受け取る設定」の「ホスト名」はバックエンドサーバーから見た名前である。そのため`target_hosts`に`localhost`を設定するとリクエストを発行したクライアントではなく、サーバーが検査対象となる。"""

	##### 全体 #####
	target_hosts: list[str] = Field([], description="検査する対象のホスト名。")
	exclude_hosts: list[str] = Field([], description="subfinderとNmapの検査から除外するホスト名やネットワーク範囲。なければ空`[]`に")
	color_output: bool = Field(True, description="標準出力の色付けを有効にするか")
	log_level: str = Field("ALL", description="出力するログのレベル")

	##### subfinder #####
	enable_subfinder: bool = Field(False, description="subfinderを使用するか")

	##### レポート機能 #####
	enable_reporting: bool = Field(False, description="レポートするか")
	report_emails: list[str] = Field([], description="レポート送信先のEメールアドレス")
	report_limit: int = Field(0, description="何個までのCVE情報をGeminiで処理するか")
	report_since: datetime = Field(datetime.fromisoformat("1970-01-01T00:00:00"), description="あるプラットフォームのバージョンが不明な場合、それの内いつ以降公開されたCVEをレポートするか")
	report_min_cvss3: float = Field(7.0, description="レポートする最小のCVSS3スコア(しきい値)")
	report_csv_encoding: str = Field("utf-8", description="レポートのCSVファイルの文字エンコーディング。設定値はそのままPythonの`open()`の`encoding`に渡される。そのためBOM付きUTF-8にしたい場合は`utf-8-sig`を指定する")
	report_enable_gemini: bool = Field(False, description="Geminiによる分析を使用するか")
	report_enable_bcc: bool = Field(False, description="CCの代わりにBCCを使うか")
	report_from: str = Field("", description="レポートのFromとして使うEメールアドレス")

	##### Nmap #####
	enable_nmap: bool = Field(False, description="Nmapを使用するか")
	nmap_extra_args: list[str] = Field([], description="Nmapに渡す追加の引数。なければ空`[]`に")

	##### Web検索機能 #####
	search_web: bool = Field(False, description="Web検索機能を使用するか")
	web_query: str = Field("", description="Web検索で使うクエリー。空文字列`\"\"`も可")
	web_region: str = Field("jp-jp", description="Web検索で使うリージョン。設定値はそのまま`DDGS.text()`に渡される。そのため[設定可能値はduckduckgo-searchを参照されたい](https://github.com/deedy5/duckduckgo_search?tab=readme-ov-file#2-text---text-search-by-duckduckgocom)")
	web_max_results: int = Field(25, description="Web検索結果の最大数。設定値はそのまま`DDGS.text()`に渡される。そのため[設定可能値はduckduckgo-searchを参照されたい](https://github.com/deedy5/duckduckgo_search?tab=readme-ov-file#2-text---text-search-by-duckduckgocom)")
	web_backend: str = Field("html", description="Web検索で使うバックエンド。設定値はそのまま`DDGS.text()`に渡される。そのため[設定可能値はduckduckgo-searchを参照されたい](https://github.com/deedy5/duckduckgo_search?tab=readme-ov-file#2-text---text-search-by-duckduckgocom)")

	##### CVE検索機能 #####
	search_cve: bool = Field(False, description="CVE検索機能を使用するか")

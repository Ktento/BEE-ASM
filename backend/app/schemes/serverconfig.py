#!/usr/bin/env python3
from pydantic import BaseModel, Field, PrivateAttr

class ServerConfigModel(BaseModel):
	"""サーバーの設定。ユーザー(クライアント)は変更できない"""
	##### パブリック。クライアントから見えても問題ないもの #####
	# the "default=" is needed to make pyright happy
	cveapi_base: str = Field(default="https://cvepremium.circl.lu/api", description="CIRCL CVE Search APIのプロトコルとホスト名を含むベースURL")
	version: str = Field(default="0.1.0", description="このASMツールサーバーのバージョン")

	enable_db: bool = Field(default=True, description="DB接続を行うか")

	##### プライベート。隠蔽したいもの #####
	_gemini_api_key: str = PrivateAttr("AIzaSyABkHvu23Sig59gKjRgd_t8PeJmt30uuQ4")
	"""Gemini ProのAPIキー"""

	# DB接続情報を設定

	host: str = PrivateAttr("mbsd-db.cpmyoiaqiinr.us-east-1.rds.amazonaws.com")
	"""EC2のパブリックIPまたはDNS名"""

	port: int = PrivateAttr(5432)
	"""PostgreSQLのデフォルトポート"""

	database: str = PrivateAttr("mbsd")
	"""データベース名"""

	user: str = PrivateAttr("mbsd")
	"""PostgreSQLのユーザー名"""

	password: str = PrivateAttr("Sangi!Bonvoyage")
	"""ユーザーパスワード"""

#!/usr/bin/env python3
from pydantic import BaseModel, Field, PrivateAttr

class ServerConfigModel(BaseModel):
	"""サーバーの設定。ユーザー(クライアント)は変更できない"""
	##### パブリック。クライアントから見えても問題ないもの #####
	# the "default=" is needed to make pyright happy
	cveapi_base: str = Field(default="https://cvepremium.circl.lu/api", description="CIRCL CVE Search APIのプロトコルとホスト名を含むベースURL")
	version: str = Field(default="0.1.0", description="このASMツールサーバーのバージョン")

	# DB接続情報を設定
	host: str = Field(default="localhost", description="EC2のパブリックIPまたはDNS名")
	port: int = Field(default=5432, description="PostgreSQLのデフォルトポート")
	database: str = Field(default="mbsd", description="データベース名")
	user: str = Field(default="mbsd", description="PostgreSQLのユーザー名")
	password: str = Field(default="Sangi!Bonvoyage", description="ユーザーパスワード")

	##### プライベート。隠蔽したいもの #####
	_gemini_api_key: str = PrivateAttr("AIzaSyABkHvu23Sig59gKjRgd_t8PeJmt30uuQ4")
	"""Gemini ProのAPIキー"""

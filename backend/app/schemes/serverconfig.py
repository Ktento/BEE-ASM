#!/usr/bin/env python3
from pydantic import BaseModel, Field

class ServerConfigModel(BaseModel):
	"""サーバーの設定。ユーザー(クライアント)は変更できない"""

	cveapi_base: str = Field("https://cvepremium.circl.lu/api", description="CIRCL CVE Search APIのプロトコルとホスト名を含むベースURL")
	version: str = Field("0.1.0", description="このASMツールサーバーのバージョン")

	# DB接続情報を設定
	host:str = Field("localhost",description="EC2のパブリックIPまたはDNS名")
	port:int = Field(5432,description="PostgreSQLのデフォルトポート")
	database:str = Field("mbsd",description="データベース名")
	user:str = Field("mbsd",description="PostgreSQLのユーザー名")
	password:str = Field("Sangi!Bonvoyage",description="ユーザーパスワード") 
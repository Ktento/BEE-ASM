#!/usr/bin/env python3
from pydantic import BaseModel, Field
from datetime import datetime

class ServerConfigModel(BaseModel):
	"""サーバーの設定。ユーザー(クライアント)は変更できない"""

	cveapi_base: str = Field("https://cvepremium.circl.lu/api", description="CIRCL CVE Search APIのプロトコルとホスト名を含むベースURL")
	version: str = Field("0.1.0", description="このASMツールサーバーのバージョン")

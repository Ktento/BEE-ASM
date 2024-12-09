#!/usr/bin/env python3
from datetime import datetime

from pydantic import BaseModel, Field

from log import Log

class LogModel(BaseModel):
	"""ログ"""

	date: datetime = Field(..., description="ログのタイムスタンプ")
	level: str = Field(..., description="ログのレベル")
	body: str = Field(..., description="ログの内容")

	@staticmethod
	def from_log(log: Log):
		return LogModel(
			date=log.date,
			# str(log.level)だと数値になることがあるため__str__()を呼び出す
			level=log.level.__str__(),
			body=log.body
		)

#!/usr/bin/env python3
from datetime import datetime, timezone
from enum import Enum
import config as Config

class Level(Enum):
	NONE = 0
	ALL = 0
	DEBUG = 1
	ERROR = 2
	WARN = 3
	INFO = 4
	FATAL = 5
	def __str__(self) -> str:
		return self.name

class Logger:
	def __init__(self, filepath) -> None:
		self.__file = None
		if filepath != None:
			self.__file = open(filepath, "a+")

	@property
	def filename(self): return self.__file.name if self.__file != None else None

	def Log(self, level: Level, text: str) -> bool:
		"""ロギングします。
		config.pyの設定により出力されなかった場合はFalseを、それ以外の場合はTrueを返します。"""

		if Config.LogLevel.value > level.value: return False
		lv = level
		# 色付けが有効ならANSIエスケープシーケンスで色付けする
		if Config.ColorOutput:
			colors = {
				# ログレベルと色の関連付け。実際に表示される色は端末の設定によって変わるが
				# ここでは一般的な色をコメントに書いてある。
				Level.DEBUG: "35",  # 紫
				Level.ERROR: "31",  # 赤
				Level.WARN:  "33",  # 黃
				Level.INFO:  "34",  # 青
				Level.FATAL: "31",  # 赤
			}
			if level in colors:
				lv = f"\033[{colors[level]}m{level}\033[m"
		date = datetime.now(timezone.utc).astimezone().isoformat()
		print(f"[{date}] [{lv}] {text}")
		if self.__file != None:
			# ログファイルは色付けない
			self.__file.write(f"[{date}] [{level}] {text}\n")
		return True

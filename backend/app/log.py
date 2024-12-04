#!/usr/bin/env python3
from datetime import datetime, timezone
from enum import Enum
from schemes.config import ConfigModel

class Level(Enum):
	"""ログのレベル。"""

	NONE = 0
	"""なし。ログ取得REST APIの`log_level`に指定すると結果のログ配列が実質的に空になります。
	バックエンド側のデベロッパーへ: `Logger.Log`の`level`にはこれを指定しないようにしてください。"""

	ALL = 100
	"""すべて。ログ取得REST APIの`log_level`に指定するとすべてのログが記録されます。
	バックエンド側のデベロッパーへ: `Logger.Log`の`level`にはこれを指定しないようにしてください。"""

	FATAL = 1
	"""回復不可能なエラー。"""

	ERROR = 2
	"""回復可能なエラー。"""

	WARN = 3
	"""警告。"""

	INFO = 4
	"""情報。"""

	DEBUG = 5
	"""デバッグ用のログ。`INFO`よりも冗長な情報を含みます。"""

	def __str__(self) -> str:
		return self.name

class Log:
	__date: datetime
	__level: Level
	__body: str

	@property
	def date(self): return self.__date

	@property
	def level(self): return self.__level

	@property
	def body(self): return self.__body

	def __init__(self, date, level, body) -> None:
		self.__date = date
		self.__level = level
		self.__body = body

	def __str__(self) -> str:
		return f"[{self.date}] [{self.level.__str__()}] {self.body}"

class Logger:
	def __init__(self, filepath: str, user_config: ConfigModel) -> None:
		self.__file = None
		self.__logs: list[Log] = []
		self.__conf = user_config
		if filepath != None:
			self.__file = open(filepath, "a+")

	@property
	def filename(self): return self.__file.name if self.__file != None else None

	@property
	def logs(self): return self.__logs.copy()

	def Log(self, level: Level, text: str) -> bool:
		"""ロギングします。"""

		lv = level
		# 色付けが有効ならANSIエスケープシーケンスで色付けする
		if self.__conf.color_output:
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
		date = datetime.now(timezone.utc).astimezone()
		self.__logs.append(Log(date, level, text))
		date = date.isoformat()
		# 標準出力に出力する場合はTrue
		enable_stdout = False
		if enable_stdout: print(f"[{date}] [{lv}] {text}")
		if self.__file != None:
			# ログファイルは色付けない
			self.__file.write(f"[{date}] [{level}] {text}\n")
		return True

	def finish(self):
		if self.__file is not None and not self.__file.closed:
			self.__file.close()

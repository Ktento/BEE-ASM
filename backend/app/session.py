#!/usr/bin/env python3
from datetime import datetime
from pathlib import Path
from typing import Any, final
from uuid import UUID, uuid4

from log import Logger
from schemes.config import ConfigModel
from schemes.progress import ProgressModel
from schemes.serverconfig import ServerConfigModel

@final
class Result():
	# Nmap
	nmap_stdout: str = ""
	nmap_stderr: str = ""

	# subfinder
	subfinder: dict[str, str] = dict()
	"""キー: ドメイン名, 値: IPアドレス"""

	# CVE
	cves: dict[str, str] = dict()
	"""キー: CPE, 値: CVE情報のJSON"""
	cve_data: list[Any] = []
	host_cpes: dict[str, set[str]] = dict()
	host_cpe_ports: dict[tuple[str, str], set[str]] = dict()
	host_ports: dict[str, set[str]] = dict()

	# DuckDuckGo
	web: str = ""

	# Report
	report_csv_all: str = ""
	report_csv_per: str = ""
	report_html: str = ""
	report_sent: bool = False

@final
class Session():
	__uuid: UUID
	__conf: ConfigModel
	__server_conf: ServerConfigModel
	__workdir: Path
	__logger: Logger
	__active: bool
	__started_at: datetime
	__progress: ProgressModel | None
	__result: Result

	def __init__(self, config: ConfigModel):
		self.__uuid = uuid4()
		self.__conf = config
		self.__server_conf = ServerConfigModel()
		self.__workdir = Path("work", str(self.__uuid))
		self.__workdir.mkdir(parents=True, exist_ok=False)
		self.__logger = Logger(filepath=str(self.__workdir / "log.txt"), user_config=self.__conf)
		self.__active = True
		self.__started_at = datetime.now()
		self.__progress = None
		self.__result = Result()

	@property
	def uuid(self): return self.__uuid

	@property
	def config(self): return self.__conf

	@property
	def server_config(self): return self.__server_conf

	@property
	def workdir(self): return self.__workdir

	@property
	def logger(self): return self.__logger

	@property
	def active(self): return self.__active

	@property
	def started_at(self): return self.__started_at

	@property
	def result(self): return self.__result

	@property
	def progress(self): return self.__progress

	def create_progress(self):
		if self.__progress is not None:
			raise Exception("The progress already created")
		self.__progress = ProgressModel(
			session_id=self.__uuid,
			started_at=datetime.now().astimezone(),
			current_tasks=[],
			task_progresses=dict()
		)

	def finish(self):
		del self.__logger

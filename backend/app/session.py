#!/usr/bin/env python3
from datetime import datetime
from pathlib import Path
from typing import final
from uuid import UUID, uuid4

from log import Logger
from schemes.config import ConfigModel
from schemes.progress import ProgressModel
from schemes.serverconfig import ServerConfigModel

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

	def __init__(self, config: ConfigModel):
		self.__uuid = uuid4()
		self.__conf = config
		self.__server_conf = ServerConfigModel(version="0.1.0", cveapi_base="https://cvepremium.circl.lu/api")
		self.__workdir = Path("work", str(self.__uuid))
		self.__workdir.mkdir(parents=True, exist_ok=False)
		self.__logger = Logger(filepath=str(self.__workdir / "log.txt"), user_config=self.__conf)
		self.__active = True
		self.__started_at = datetime.now()
		self.__progress = None

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

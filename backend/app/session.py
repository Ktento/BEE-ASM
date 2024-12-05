#!/usr/bin/env python3
import os
from datetime import datetime
from pathlib import Path
from typing import final, List
from uuid import UUID, uuid4
from context import Context
from schemes.config import ConfigModel
from schemes.serverconfig import ServerConfigModel
from log import Logger

@final
class Session():
	__uuid: UUID
	__conf: ConfigModel
	__server_conf: ServerConfigModel
	__workdir: Path
	__logger: Logger
	__active: bool
	__started_at: datetime

	def __init__(self, config: ConfigModel):
		self.__uuid = uuid4()
		self.__conf = config
		self.__server_conf = ServerConfigModel(version="0.1.0", cveapi_base="https://cvepremium.circl.lu/api")
		self.__workdir = Path("work", str(self.__uuid))
		self.__workdir.mkdir(parents=True, exist_ok=False)
		self.__logger = Logger(filepath=str(self.__workdir / "log.txt"), user_config=self.__conf)
		self.__active = True
		self.__started_at = datetime.now()

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

	def finish(self):
		del self.__logger

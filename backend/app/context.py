#!/usr/bin/env python3
from log import Logger
from schemes.config import ConfigModel

class Context:
	def __init__(self, logger: Logger, savedir: str, hosts: list, config: ConfigModel | None) -> None:
		self.__savedir = savedir
		self.__logger = logger
		self.__hosts = hosts
		self.__config = config

	@property
	def savedir(self): return self.__savedir

	@property
	def logger(self): return self.__logger

	@property
	def hosts(self): return  self.__hosts

	@hosts.setter
	def hosts(self, value): self.__hosts = value

	@property
	def config(self): return self.__config

	@config.setter
	def config(self, value): self.__config = value

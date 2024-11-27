#!/usr/bin/env python3
from log import Logger

class Context:
	def __init__(self, logger: Logger, savedir: str, hosts: list) -> None:
		self.__savedir = savedir
		self.__logger = logger
		self.__hosts = hosts

	@property
	def savedir(self): return self.__savedir

	@property
	def logger(self): return self.__logger

	@property
	def hosts(self): return  self.__hosts

	@hosts.setter
	def hosts(self, value): self.__hosts = value

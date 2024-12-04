#!/usr/bin/env python3
from uuid import UUID
from typing import final, List
from schemes.config import ConfigModel
from session import Session

@final
class Singleton(type):
	__insts = {}
	def __call__(cls, *args, **kwargs):
		if cls not in cls.__insts:
			cls.__insts[cls] = super(Singleton, cls).__call__(*args, **kwargs)
		return cls.__insts[cls]

@final
class SessionManager(metaclass=Singleton):
	# UUIDからセッションを探しやすくするために辞書型にする
	__sessions: dict[UUID, Session]

	def __init__(self):
		self.__sessions = dict()

	def create_session(self, config: ConfigModel):
		s = Session(config)
		self.__sessions[s.uuid] = s
		return s

	def find_session(self, uuid: UUID) -> Session | None:
		return self.__sessions[uuid] if uuid in self.__sessions else None

	def destroy_session(self, uuid: UUID) -> None:
		s = self.find_session(uuid)
		if s is None:
			raise KeyError("session not found")
		s.finish()
		del self.__sessions[uuid]

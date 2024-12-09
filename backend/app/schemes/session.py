#!/usr/bin/env python3
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from schemes.config import ConfigModel
from schemes.serverconfig import ServerConfigModel
from session import Session

class SessionModel(BaseModel):
	"""セッションを表します。"""

	session_id: UUID = Field(..., description="セッションの識別子")
	config: ConfigModel = Field(..., description="設定されているユーザー設定")
	server_config: ServerConfigModel = Field(..., description="設定されているサーバー設定")
	workdir: str = Field(..., description="バックエンド上の作業ディレクトリー")
	active: bool = Field(..., description="セッションが有効であるか")
	started_at: datetime = Field(..., description="セッション開始時刻")

	@staticmethod
	def from_session(session: Session):
		return SessionModel(
			session_id=session.uuid,
			config=session.config,
			server_config=session.server_config,
			workdir=str(session.workdir),
			active=session.active,
			started_at=session.started_at
		)

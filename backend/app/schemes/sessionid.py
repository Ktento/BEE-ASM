#!/usr/bin/env python3
from uuid import UUID

from pydantic import BaseModel, Field

class SessionIdModel(BaseModel):
	"""セッションIDのみを持つモデルです。"""

	session_id: UUID = Field(..., description="セッションの識別子")

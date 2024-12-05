#!/usr/bin/env python3
from datetime import datetime, timezone
from uuid import UUID
from fastapi import Depends, APIRouter, Response
from fastapi.exceptions import HTTPException
from log import Level
from routers.session import ensure_session
from schemes.config import ConfigModel
from schemes.session import SessionModel
from schemes.log import LogModel
from singleton import SessionManager
from session import Session
from schemes.progress import ProgressModel

router = APIRouter(tags=["進捗"])


@router.get(
	"/progress/show",
	responses={
		404: {"description": "セッションが存在しない場合、またはASMを開始していない場合"}
	}
)
def get_progress_status(
	session: Session = Depends(ensure_session),
) -> ProgressModel:
	if session.progress is None:
		raise HTTPException(404, "asm_not_started_yet")
	return session.progress

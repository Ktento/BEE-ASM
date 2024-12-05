#!/usr/bin/env python3
from datetime import datetime, timezone
from uuid import UUID
from fastapi import BackgroundTasks, Depends, APIRouter, Response
from fastapi.exceptions import HTTPException
from asm.asm import Asm
from log import Level
from routers.session import ensure_session
from schemes.config import ConfigModel
from schemes.session import SessionModel
from schemes.log import LogModel
from singleton import SessionManager
from session import Session
from schemes.progress import ProgressModel

router = APIRouter(tags=["ASM"])


@router.post(
	"/asm/execute",
	responses={
		404: {"description": "セッションが存在しない場合"},
		409: {"description": "すでにASMが開始されている場合"}
	}
)
async def run_asm(
	background_tasks: BackgroundTasks,
	session: Session = Depends(ensure_session)
) -> ProgressModel:
	if session.progress is not None:
		raise HTTPException(409, "asm_already_started")

	session.create_progress()
	assert session.progress is not None

	background_tasks.add_task(Asm, session)

	return session.progress

#!/usr/bin/env python3
from fastapi import APIRouter, BackgroundTasks
from fastapi.exceptions import HTTPException

from asm.asm import Asm
from routers.session import ensure_session
from schemes.progress import ProgressModel
from schemes.sessionid import SessionIdModel

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
	data: SessionIdModel
) -> ProgressModel:
	session = ensure_session(data.session_id)

	if session.progress is not None:
		raise HTTPException(409, "asm_already_started")

	session.create_progress()
	assert session.progress is not None

	background_tasks.add_task(Asm, session)

	return session.progress

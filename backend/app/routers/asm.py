#!/usr/bin/env python3
from fastapi import APIRouter, BackgroundTasks, Depends
from fastapi.exceptions import HTTPException

from asm.asm import Asm
from routers.session import ensure_session
from schemes.progress import ProgressModel
from session import Session

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

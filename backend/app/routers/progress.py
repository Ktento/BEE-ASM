#!/usr/bin/env python3
from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException

from routers.session import ensure_session
from schemes.progress import ProgressModel
from session import Session

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

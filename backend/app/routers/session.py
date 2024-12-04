#!/usr/bin/env python3
from datetime import datetime
from uuid import UUID
from fastapi import Depends, APIRouter, Response
from fastapi.exceptions import HTTPException
from log import Level
from schemes.config import ConfigModel
from schemes.session import SessionModel
from schemes.log import LogModel
from singleton import SessionManager

router = APIRouter(tags=["セッション"])

@router.post("/session/create")
def new_session(config: ConfigModel) -> SessionModel:
	"""新規セッションを開始します"""
	r = SessionManager().create_session(config)
	return SessionModel.from_session(r)


@router.get(
	"/session/show/{session_id}",
	responses={
		404: {"description": "セッションが存在しない場合"}
	}
)
def get_session_info(session_id: UUID) -> SessionModel:
	"""指定されたセッションの情報を表示します"""
	s = SessionManager().find_session(session_id)
	if s is None:
		raise HTTPException(404, "session_not_found")
	return SessionModel.from_session(s)


@router.delete(
	"/session/destroy/{session_id}", status_code=204,
	responses={
		204: {"description": "セッションを正常に終了できた場合"},
		404: {"description": "セッションが存在しない場合"}
	}
)
def destroy_session(session_id: UUID):
	"""セッションを終了します"""
	try:
		SessionManager().destroy_session(session_id)
	except KeyError:
		raise HTTPException(404, "session_not_found")
	return Response(status_code=204)

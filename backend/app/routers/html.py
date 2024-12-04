#!/usr/bin/env python3
from fastapi import APIRouter, Response
from fastapi.responses import FileResponse, HTMLResponse

router = APIRouter(tags=["Webブラウザーヘルパー"])

@router.get("/", response_class=HTMLResponse)
def get_index_html():
	"""WebブラウザーがこのバックエンドREST APIサーバーにアクセスした際のためにHTMLドキュメントを返します"""
	data = """\
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE html>
<html lang="en">
	<head>
		<title>The backend server of ASMTool</title>
	</head>
	<body>
		<a href="/docs">See the Swagger UI</a>
		<a href="/docs">or Redoc.</a>
	</body>
</html>
"""
	responce = HTMLResponse(content=data)
	return responce


@router.get("/favicon.ico", response_class=FileResponse)
def get_favicon() -> FileResponse:
	"""Faviconを返します"""
	return FileResponse("favicon.ico", media_type="image/vnd.microsoft.icon")

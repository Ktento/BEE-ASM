#!/usr/bin/env python3
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import asm, html, log, progress, session

app = FastAPI()

app.include_router(html.router)
app.include_router(session.router)
app.include_router(log.router)
app.include_router(progress.router)
app.include_router(asm.router)

# python3 -m uvicorn fastapi_main:app --reload

# CORS ミドルウェアを追加
app.add_middleware(
	CORSMiddleware,
	allow_origins=["http://ec2-34-229-220-192.compute-1.amazonaws.com"],  # フロントエンドのオリジンを許可
	allow_credentials=True,
	allow_methods=["*"],  # 全てのHTTPメソッドを許可
	allow_headers=["*"],  # 全てのHTTPヘッダーを許可
)

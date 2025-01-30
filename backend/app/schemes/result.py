#!/usr/bin/env python3
from typing import Any, Optional

from pydantic import BaseModel, Field, Json

class HostCpePortsModel(BaseModel):
	host: str
	cpe: str
	ports: set[str]

class ResultSubfinderModel(BaseModel):
	"""subfinderの結果"""
	hosts: dict[str, str] = Field(default=dict(), description="subfinderで見つかったホスト。キー: ドメイン名, 値: IPアドレス")

class ResultNmapModel(BaseModel):
	"""Nmapの結果"""
	result: str = Field(default="", description="Nmapの実行結果(XML形式)")
	stderr: str = Field(default="", description="Nmapの標準エラー出力(stderr, プレーンテキスト)")
	host_cpes: Optional[dict[str, set[str]]] = Field(default=None, description="ホストとそのホストが持つCPE文字列")
	host_cpe_ports: Optional[list[HostCpePortsModel]] = Field(default=None, description="ホストとCPE文字列の組が持つプロトコルとポート番号")
	host_ports: Optional[dict[str, set[str]]] = Field(default=None, description="ホストとそのホストが持つプロトコルとポート番号")

class ResultCveModel(BaseModel):
	"""CVE検索の結果"""
	cves: dict[str, Json] = Field(default=dict(), description="CVE情報のJSON。キーはCPE文字列で値はCVE情報")
	cve_data: Optional[list[Any]] = Field(default=None, description="CVEデータ")

class ResultWebSearchModel(BaseModel):
	"""Web検索の結果"""
	result: Json = Field(default="[]", description="Web検索結果のJSON")

class ResultReportModel(BaseModel):
	"""レポートの結果"""
	csv_all: str = Field(default="", description="全ホストをまとめたレポートのCSV")
	csv_per: str = Field(default="", description="ホストごとにまとめたレポートのCSV")
	html: str = Field(default="", description="レポートのHTML文書。<html>タグを含むフルのHTMLドキュメント")
	mail_sent: bool = Field(default=False, description="メールが送信されたか")

class ResultModel(BaseModel):
	"""全結果"""
	subfinder: Optional[ResultSubfinderModel] = Field(default=None)
	nmap: Optional[ResultNmapModel] = Field(default=None)
	cve: Optional[ResultCveModel] = Field(default=None)
	websearch: Optional[ResultWebSearchModel] = Field(default=None)
	reporting: Optional[ResultReportModel] = Field(default=None)

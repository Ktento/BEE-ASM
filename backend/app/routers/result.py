#!/usr/bin/env python3
from fastapi import APIRouter, Depends

from routers.session import ensure_session
from schemes.result import (
	HostCpePortsModel,
	ResultCveModel,
	ResultModel,
	ResultNmapModel,
	ResultReportModel,
	ResultSubfinderModel,
	ResultWebSearchModel,
)
from session import Session

router = APIRouter(tags=["結果"])


@router.get(
	"/result/show",
	responses={
		404: {"description": "セッションが存在しない場合"}
	}
)
def show(
	session: Session = Depends(ensure_session),
) -> ResultModel:
	"""ASMの実行結果を返します。"""
	r = ResultModel()

	if session.config.enable_nmap:
		try: r.nmap = ResultNmapModel(
			result=session.result.nmap_stdout,
			stderr=session.result.nmap_stderr,
			host_cpes=session.result.host_cpes,
			host_cpe_ports=[HostCpePortsModel(host=k[0], cpe=k[1], ports=session.result.host_cpe_ports[k]) for k in session.result.host_cpe_ports.keys()],
			host_ports=session.result.host_ports
		)
		except: pass

	if session.config.enable_subfinder or session.config.enable_nmap:
		try: r.subfinder = ResultSubfinderModel(hosts=session.result.subfinder)
		except: pass

	if session.config.enable_reporting:
		try: r.reporting = ResultReportModel(
			csv_all=session.result.report_csv_all,
			csv_per=session.result.report_csv_per,
			html=session.result.report_html,
			mail_sent=session.result.report_sent
		)
		except: pass

	if session.config.search_web:
		try: r.websearch = ResultWebSearchModel(result=session.result.web)
		except: pass

	if session.config.search_cve:
		try: r.cve = ResultCveModel(
			cves=session.result.cves,
			cve_data=session.result.cve_data,
		)
		except: pass

	return r

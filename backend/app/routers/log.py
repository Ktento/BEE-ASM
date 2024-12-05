#!/usr/bin/env python3
from datetime import datetime, timezone
from uuid import UUID
from fastapi import Depends, APIRouter, Response
from fastapi.exceptions import HTTPException
from log import Level
from schemes.config import ConfigModel
from schemes.session import SessionModel
from schemes.log import LogModel
from singleton import SessionManager

router = APIRouter(tags=["ログ"])


@router.get(
	"/log/show_by_date",
	responses={
		404: {"description": "セッションが存在しない場合"}
	}
)
def show_by_date(
	session_id: UUID,
	since: datetime = datetime(1970, 1, 1, tzinfo=timezone.utc),
	until: datetime = datetime(2100, 1, 1, tzinfo=timezone.utc),
	limit: int = -1,
	level: str = Level.ALL.__str__()
) -> list[LogModel]:
	"""タイムスタンプからログを抽出します。

	`since`と`until`で指定できる期間は半開区間（左閉右開）です。
	つまり`since`はinclusive、`until`はexclusiveです。
	この期間内に記録されたログを返します。
	なおタイムスタンプにはタイムゾーン情報が必須です。
	例えば`2010-01-31T12:50:30`はエラーになります。
	そのため`2010-01-31T12:50:30+09:00`や`2010-01-31T12:50:30Z`のように何らかのタイムゾーン情報を指定するようにしてください。

	`limit`には古いものから最大の何個のログを出力するかを指定します。結果として返されるログの数は`limit`より少なくなることもあります。
	負数を指定すると(`since`, `until`で指定された期間に一致する)すべてのログを返します。

	`level`には出力するログのレベルを指定します。重要度が高いレベルの順番を(`NONE`)→`FATAL`→`ERROR`→`WARN`→`INFO`→`DEBUG`→(`ALL`)のように定義したとき
	重要度が`level`以上であるログを抽出します。例えば`level`に`WARN`を指定した際、`FATAL`, `ERROR`, `WARN`のログが抽出されます。`INFO`, `DEBUG`のログは出力されません。
	`ALL`を指定するとすべてのレベルのログを出力します。`NONE`を指定すると結果は空の配列`[]`になります。

	流れとしては
	全ログ → タイムスタンプでフィルター → `level`でフィルター → `limit`でフィルター
	のようになります。

	結果はタイムスタンプの昇順になります。"""
	if level not in Level.__members__:
		raise HTTPException(422, "invalid_log_level")
	if since.tzinfo is None or until.tzinfo is None:
		raise HTTPException(422, "timestamp_must_have_timezone")
	lv: Level = Level[level]
	s = SessionManager().find_session(session_id)
	if s is None:
		raise HTTPException(404, "session_not_found")
	# loggerのログはすでにタイムスタンプの昇順でソートされていると思われるが
	# ここでは念のために再ソートしておく
	logs = sorted(s.logger.logs, key=lambda x: x.date)
	return \
		[LogModel.from_log(i) for i in logs if since <= i.date and i.date < until and i.level.value <= lv.value] \
		if limit < 0 else \
		[LogModel.from_log(i) for i in logs if since <= i.date and i.date < until and i.level.value <= lv.value][:limit]

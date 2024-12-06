#!/usr/bin/env python3
from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import AfterValidator, BaseModel, Field, computed_field

def _check_zero_to_one(v: float) -> float:
	assert 0.0 <= v and v <= 1.0
	return v

ZeroToOneFloat = Annotated[float, AfterValidator(_check_zero_to_one)]
"""`0.0`以上`1.0`以下の`float`です。"""

TaskName = str

class ProgressModel(BaseModel):
	"""進捗状況を表します。"""

	session_id: UUID = Field(..., description="セッションの識別子")
	started_at: datetime = Field(..., description="セッション開始時刻")
	# 後に並列化する場合に備えてここではリストとして定義してある
	current_tasks: list[TaskName] = Field(..., description="実行している機能名")
	task_progresses: dict[TaskName, ZeroToOneFloat] = Field(..., description="機能の進捗状況")

	@computed_field
	@property
	def overall_progress(self) -> ZeroToOneFloat:
		"""全体の進捗状況"""

		if len(self.task_progresses) == 0: return 0.0

		# 全進捗の平均を取って
		value = sum(self.task_progresses.values()) / len(self.task_progresses)
		# 確実に0以上1以下に収める
		return max(min(value, 1.0), 0.0)

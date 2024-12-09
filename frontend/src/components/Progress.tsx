import {
  CircleProgress,
  CircleProgressLabel,
  Box,
  Text,
  Progress as LinearProgress,
} from "@yamada-ui/react";
import { useEffect } from "react";
import { ProgressesRes } from "../types/Progress";
import { ApiService } from "../services/ApiService";

interface Props {
  sessionId: string;
  overallProgress: number;
  taskProgresses: Record<string, number>;
  setOverallProgress: React.Dispatch<React.SetStateAction<number>>;
  setTaskProgresses: React.Dispatch<
    React.SetStateAction<Record<string, number>>
  >;
}

function Progress(props: Props) {
  const {
    sessionId,
    overallProgress,
    taskProgresses,
    setOverallProgress,
    setTaskProgresses,
  } = props;

  useEffect(() => {
    if (!sessionId) {
      console.log("not found session id");
      return;
    }

    const fetchProgress = async () => {
      const data: ProgressesRes | null = await ApiService.getInstance().get(
        `progress/show?session_id=${sessionId}`
      );
      if (!data) return;

      setOverallProgress(Math.round(data.overall_progress * 100));
      setTaskProgresses(data.task_progresses);
    };

    const interval = setInterval(() => {
      fetchProgress();
    }, 5000);

    fetchProgress();

    return () => clearInterval(interval);
  }, [sessionId, setOverallProgress, setTaskProgresses]);

  return (
    <Box>
      <Box display="flex" flexDirection="column" alignItems="center" mb={8}>
        <CircleProgress min={0} max={100} value={overallProgress} size="150px">
          <CircleProgressLabel>{overallProgress}%</CircleProgressLabel>
        </CircleProgress>
        <Text mt={4} fontWeight="bold">
          全体進捗
        </Text>
      </Box>

      <Box>
        <Text fontWeight="bold" mb={4}>
          各タスク進捗
        </Text>
        {Object.entries(taskProgresses).map(([task, progress]) => (
          <Box key={task} mb={4}>
            <Text fontWeight="medium">{task}:</Text>
            <LinearProgress
              value={Math.round(progress * 100)}
              colorScheme={progress === 1.0 ? "green" : "purple"}
              mb={2}
            />
            <Text>{Math.round(progress * 100)}%</Text>
          </Box>
        ))}
      </Box>
    </Box>
  );
}

export default Progress;

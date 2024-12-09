import {
  CircleProgress,
  CircleProgressLabel,
  Box,
  Text,
  Progress as LinearProgress,
} from "@yamada-ui/react";
import { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";

function Progress() {
  const [overallProgress, setOverallProgress] = useState(0);
  const [taskProgresses, setTaskProgresses] = useState<Record<string, number>>(
    {}
  );
  const ENDPOINT: string = import.meta.env.VITE_END_POINT;

  const location = useLocation();
  const sessionId = location.state?.sessionId;

  useEffect(() => {
    if (!sessionId) {
      console.log("not found session id");
      return;
    }

    const fetchProgress = async () => {
      try {
        const header = new Headers();
        header.append("Content-Type", "application/json");

        const response = await fetch(
          `${ENDPOINT}/progress/show?session_id=${sessionId}`,
          {
            method: "GET",
            headers: header,
          }
        );

        if (!response.ok) {
          console.log("error");
          console.log(response);
          return;
        }

        const data = await response.json();
        if (data) {
          if (typeof data.overall_progress === "number") {
            setOverallProgress(Math.round(data.overall_progress * 100));
          }
          if (
            data.task_progresses &&
            typeof data.task_progresses === "object"
          ) {
            setTaskProgresses(data.task_progresses);
          }
        }
      } catch (error) {
        console.error("Error fetching progress:", error);
      }
    };

    const interval = setInterval(() => {
      fetchProgress();
    }, 5000);

    fetchProgress();

    return () => clearInterval(interval);
  }, [ENDPOINT, sessionId]);

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

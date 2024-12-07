import { CircleProgress, CircleProgressLabel } from "@yamada-ui/react";
import { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";

function Progress() {
  const [progress, setProgress] = useState(0);
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
        if (data && typeof data.overall_progress === "number") {
          setProgress(Math.round(data.overall_progress * 100));
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
    <CircleProgress min={0} max={100} value={progress}>
      <CircleProgressLabel>{progress}%</CircleProgressLabel>
    </CircleProgress>
  );
}

export default Progress;

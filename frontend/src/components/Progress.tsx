import { CircleProgress, CircleProgressLabel } from "@yamada-ui/react";
import { useEffect, useState } from "react";

function Progress() {
  const [progress, setProgress] = useState(0);
  const ENDPOINT: string = import.meta.env.VITE_END_POINT;

  useEffect(() => {
    const fetchProgress = async () => {
      try {
        const response = await fetch(`${ENDPOINT}/progress`);
        if (!response.ok) throw new Error("Failed to fetch progress");
        const data = await response.json();
        if (data && typeof data.progress === "number")
          setProgress(data.progress);
      } catch (error) {
        console.error("Error fetching progress:", error);
      }
    };

    const interval = setInterval(() => {
      fetchProgress();
    }, 5000);

    return () => clearInterval(interval);
  }, [ENDPOINT]);

  return (
    <CircleProgress min={0} max={100} value={progress}>
      <CircleProgressLabel>{progress}%</CircleProgressLabel>
    </CircleProgress>
  );
}

export default Progress;

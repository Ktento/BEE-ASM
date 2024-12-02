import { CircleProgress, CircleProgressLabel } from "@yamada-ui/react";
import { useEffect, useState } from "react";

function Progress() {
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    // TODO: add fetch progress
    const interval = setInterval(() => {
      setProgress((prev) => (prev + 10 > 100 ? 100 : prev + 10));
    }, 5000);

    return () => clearInterval(interval);
  }, []);

  return (
    <CircleProgress min={0} max={100} value={progress}>
      <CircleProgressLabel>{progress}%</CircleProgressLabel>
    </CircleProgress>
  );
}

export default Progress;

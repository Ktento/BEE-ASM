import { Box, Button, Heading } from "@yamada-ui/react";
import Progress from "../components/Progress";
import { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import { Result } from "../types/Restult";
import { ResultPanel } from "../components/ResultPanel";

function Success() {
  const location = useLocation();
  const sessionId = location.state?.sessionId;
  const ENDPOINT: string = import.meta.env.VITE_END_POINT;

  const [overallProgress, setOverallProgress] = useState(0);
  const [taskProgresses, setTaskProgresses] = useState<Record<string, number>>(
    {}
  );
  const [result, setResult] = useState<Result | undefined>(undefined);

  useEffect(() => {
    if (overallProgress < 100 || !sessionId) return;

    const fetchResult = async () => {
      const header = new Headers();
      header.append("Content-Type", "application/json");

      try {
        const response = await fetch(
          `${ENDPOINT}/result/show?session_id=${sessionId}`,
          {
            method: "GET",
            headers: header,
          }
        );
        if (!response.ok) return;

        const data = await response.json();
        if (data) {
          setResult(data);
        }
      } catch (e) {
        console.log(e);
      }
    };

    fetchResult();
  }, [overallProgress, sessionId]);

  if (!sessionId) {
    // Todo: add sorry page
    return (
      <Box>
        <Heading>セッションが見つかりません。</Heading>
      </Box>
    );
  }

  return (
    <Box as={"main"} p={5}>
      <Box p={5} display={"flex"} justifyContent={"space-between"}>
        <Heading>送信が成功しました！</Heading>
        <Button
          colorScheme="purple"
          onClick={() => (window.location.href = "/")}
        >
          ホームに戻る
        </Button>
      </Box>
      <Box p={5}>
        {overallProgress < 100 && (
          <>
            <Heading as={"h3"} size={"lg"}>
              進捗情報
            </Heading>
            <Progress
              sessionId={sessionId}
              overallProgress={overallProgress}
              taskProgresses={taskProgresses}
              setOverallProgress={setOverallProgress}
              setTaskProgresses={setTaskProgresses}
            />
          </>
        )}
        {result && (
          <Box>
            <Heading>結果</Heading>
            <ResultPanel result={result} />
          </Box>
        )}
      </Box>
    </Box>
  );
}

export default Success;

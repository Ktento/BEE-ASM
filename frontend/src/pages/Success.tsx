import { Box, Button, Heading } from "@yamada-ui/react";
import Progress from "../components/Progress";
import { useState } from "react";
import { useLocation } from "react-router-dom";

function Success() {
  const location = useLocation();
  const sessionId = location.state?.sessionId;

  const [overallProgress, setOverallProgress] = useState(0);
  const [taskProgresses, setTaskProgresses] = useState<Record<string, number>>(
    {}
  );

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
      </Box>
    </Box>
  );
}

export default Success;

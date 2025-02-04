import {
  Box,
  Button,
  Heading,
  Modal,
  ModalBody,
  ModalFooter,
  ModalHeader,
  Text,
} from "@yamada-ui/react";
import Progress from "../components/Progress";
import { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import { Result } from "../types/Restult";
import { ResultPanel } from "../components/ResultPanel";
import { ApiService } from "../services/ApiService";
import { ResultGraphCvss } from "../components/ResultGraphCvss";

function Success() {
  const location = useLocation();
  const sessionId = location.state?.sessionId;

  const [overallProgress, setOverallProgress] = useState(0);
  const [taskProgresses, setTaskProgresses] = useState<Record<string, number>>(
    {}
  );
  const [result, setResult] = useState<Result | undefined>(undefined);
  const [isOpen, setIsOpen] = useState(false);

  useEffect(() => {
    if (overallProgress < 100 || !sessionId) return;

    const fetchResult = async () => {
      const data: Result | null = await ApiService.getInstance().get(
        `result/show?session_id=${sessionId}`
      );
      if (!data) return;
      setResult(data);
    };

    fetchResult();
  }, [overallProgress, sessionId]);

  const handleBackHome = () => {
    setIsOpen(false);
    const fetchDeleteSession = async () => {
      await ApiService.getInstance().delete(
        `session/destroy?session_id=${sessionId}`
      );

      window.location.href = "/";
    };

    fetchDeleteSession();
    setIsOpen(false);
  };

  if (!sessionId) {
    return (
      <Box>
        <Heading>セッションが見つかりません。</Heading>
      </Box>
    );
  }

  return (
    <Box as={"main"} p={5}>
      <Box p={5} display={"flex"} justifyContent={"space-between"}>
        <Heading>{result ? "結果" : "送信が成功しました！"}</Heading>
        {result && <ResultGraphCvss result={result} />}
        <Button colorScheme="purple" onClick={() => setIsOpen(true)}>
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
        {result && <ResultPanel result={result} />}
      </Box>
      <Modal open={isOpen} onClose={() => setIsOpen(false)}>
        <ModalHeader>ホームに戻る</ModalHeader>

        <ModalBody>
          <Text>セッションが削除されますがよろしいですか?</Text>
        </ModalBody>

        <ModalFooter>
          <Button variant="ghost" onClick={() => setIsOpen(false)}>
            いいえ
          </Button>
          <Button colorScheme="primary" onClick={handleBackHome}>
            はい
          </Button>
        </ModalFooter>
      </Modal>
    </Box>
  );
}

export default Success;

import { Box, Button, Heading } from "@yamada-ui/react";
import Progress from "../components/Progress";

function Success() {
  return (
    <Box as={"main"} p={5}>
      <Heading>送信が成功しました！</Heading>
      <Box>
        <Heading as={"h2"}>進捗情報</Heading>
        <Progress />
      </Box>
      <Box p={5}>
        <Button
          colorScheme="purple"
          onClick={() => (window.location.href = "/")}
        >
          ホームに戻る
        </Button>
      </Box>
    </Box>
  );
}

export default Success;

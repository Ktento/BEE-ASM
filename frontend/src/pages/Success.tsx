import { Box, Button, Heading } from "@yamada-ui/react";

function Success() {
  return (
    <Box as={"main"} p={5}>
      <Heading>送信が成功しました！</Heading>
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

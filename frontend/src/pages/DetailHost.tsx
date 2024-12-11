import { Box, Text } from "@yamada-ui/react";
import { useLocation } from "react-router-dom";
import { CVEInfo } from "../types/Restult";

export const DetailHost = () => {
  const location = useLocation();
  const cves = location.state?.cves as { [key: string]: CVEInfo[] };
  console.log(cves);

  return (
    <Box>
      <Text>aaa</Text>
    </Box>
  );
};

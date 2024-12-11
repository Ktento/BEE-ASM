import { Text, Box, Flex } from "@yamada-ui/react";
import { PieChart, CellProps } from "@yamada-ui/charts";
import { Result } from "../types/Restult";
import { useMemo } from "react";

interface Props {
  result: Result;
}

export const ResultGraphCvss = (props: Props) => {
  const { result } = props;
  if (!result.cve || !result.cve.cves) {
    return <Text>No CVE data available.</Text>;
  }
  const ranges = {
    Low: 0, // 0.1 ~ 3.9
    Medium: 0, // 4.0 ~ 6.9
    High: 0, // 7.0 ~ 8.9
    Critical: 0, // 9.0 ~ 10.0
  };

  for (const [, cveList] of Object.entries(result.cve.cves)) {
    cveList.forEach((cveInfo) => {
      if (cveInfo.cvss !== undefined) {
        const cvss = cveInfo.cvss;
        if (cvss >= 0.1 && cvss <= 3.9) {
          ranges.Low += 1;
        } else if (cvss >= 4.0 && cvss <= 6.9) {
          ranges.Medium += 1;
        } else if (cvss >= 7.0 && cvss <= 8.9) {
          ranges.High += 1;
        } else if (cvss >= 9.0 && cvss <= 10.0) {
          ranges.Critical += 1;
        }
      }
    });
  }

  const mewtwo: CellProps[] = useMemo(
    () => [
      {
        name: "Critical",
        value: ranges.Critical,
        color: "#f41907", // 赤,
      },
      {
        name: "High",
        value: ranges.High,
        color: "#f66e0b", // 橙
      },
      {
        name: "Medium",
        value: ranges.Medium,
        color: "#fbbc04", // 黄
      },
      {
        name: "Low",
        value: ranges.Low,
        color: "#21b803", // 緑
      },
    ],
    []
  );
  return (
    <Flex direction="row" align="center" gap={8}>
      {/* 円グラフ */}
      <PieChart data={mewtwo} />

      {/* 名前ラベル */}
      <Box>
        {mewtwo.map((data) => (
          <Flex key={data.name} align="center" gap={2}>
            <Box
              w={4}
              h={4}
              bgColor={data.color}
              borderRadius="full"
              border="1px solid black"
            />
            <Text fontWeight="bold">
              {data.name}: {data.value}
            </Text>
          </Flex>
        ))}
      </Box>
    </Flex>
  );
};

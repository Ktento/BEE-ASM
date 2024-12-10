import { Text } from "@yamada-ui/react";
import { PieChart } from "@yamada-ui/charts";
import { CVEInfo, Result } from "../types/Restult";

interface Props {
  result: Result;
}

export const ResultPanel = (props: Props) => {
  const { result } = props;
  console.log(result.cve);
  if (!result.cve || !result.cve.cves) {
    return <Text>No CVE data available.</Text>;
  }

  // CVSS を一つずつ取り出す
  const cvssScores: { cpe: string; cvss: number }[] = [];

  for (const [cpe, cveList] of Object.entries(result.cve.cves)) {
    cveList.forEach((cveInfo) => {
      if (cveInfo.cvss !== undefined) {
        cvssScores.push({ cpe, cvss: cveInfo.cvss });
      }
    });
  }

  const mewtwo: CellProps[] = useMemo(
    () => [
      {
        name: "Low",
        value: 106,
        color: "green.500",
      },
      {
        name: "Medium",
        value: 110,
        color: "red.500",
      },
      {
        name: "High",
        value: 90,
        color: "blue.500",
      },
      {
        name: "Critical",
        value: 154,
        color: "purple.500",
      },
    ],
    []
  );

  return <PieChart data={mewtwo} />;
};

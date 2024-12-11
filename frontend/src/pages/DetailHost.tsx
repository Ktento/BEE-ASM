import { Box, Button, Heading, Text } from "@yamada-ui/react";
import { useLocation, useNavigate } from "react-router-dom";
import { CVEInfo } from "../types/Restult";

export const DetailHost = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const cves = location.state?.cves as { [key: string]: CVEInfo[] };
  const host = location.state?.host as string;
  const cpes = location.state?.cpes as string[];

  const getBackgroundColor = (cvss?: number) => {
    if (cvss === undefined) return "#ffffff"; // デフォルトの白
    if (cvss >= 0.1 && cvss <= 3.9) return "#21b803"; // Low (緑)
    if (cvss >= 4.0 && cvss <= 6.9) return "#fbbc04"; // Medium (黄)
    if (cvss >= 7.0 && cvss <= 8.9) return "#f66e0b"; // High (橙)
    if (cvss >= 9.0 && cvss <= 10.0) return "#f41907"; // Critical (赤)
    return "#ffffff";
  };

  return (
    <Box as={"main"} p={5}>
      <Box p={5} display={"flex"} justifyContent={"space-between"}>
        <Heading>{host}の結果</Heading>
        <Button colorScheme="purple" onClick={() => navigate(-1)}>
          前のページに戻る
        </Button>
      </Box>

      {cpes.length > 0 ? (
        <Box overflowY={"auto"}>
          <table>
            <thead>
              <tr>
                <th>CPE</th>
                <th>CVE-ID</th>
                <th>CVSS</th>
                <th>発行日</th>
                <th>説明</th>
              </tr>
            </thead>
            <tbody>
              {cpes.map((cpe) => {
                const targetCve = cves[cpe];

                return targetCve.map((cve) => {
                  return (
                    <tr key={cve.id}>
                      <td>{cpe}</td>
                      <td>{cve.id}</td>
                      <td
                        style={{
                          backgroundColor: getBackgroundColor(cve.cvss),
                        }}
                      >
                        {cve.cvss ? cve.cvss : "NONE"}
                      </td>
                      <td>{cve.Published}</td>
                      <td>{cve.summary}</td>
                    </tr>
                  );
                });
              })}
            </tbody>
          </table>
        </Box>
      ) : (
        <Text>脆弱性は見つかりませんでした。</Text>
      )}
    </Box>
  );
};

import { Box, Heading, List, ListItem, Text } from "@yamada-ui/react";
import { CVEInfo, Result } from "../types/Restult";

interface Props {
  result: Result;
}

export const ResultPanel = (props: Props) => {
  const { result } = props;

  // ホスト情報がない場合の処理
  if (!result.subfinder || !result.subfinder.hosts) {
    return (
      <Box p={5}>
        <Heading size="md">ホスト情報が見つかりません。</Heading>
      </Box>
    );
  }

  return (
    <Box p={5}>
      <Heading size="lg">ホストごとの脆弱性</Heading>
      {Object.entries(result.subfinder.hosts).map(([host, ip]) => {
        // 該当ホストに関連するCVE情報を抽出
        const relatedCves = result.cve?.cves?.[host] || [];

        return (
          <Box key={host} mt={5} p={4} borderWidth="1px" borderRadius="lg">
            <Heading size="md">{host}</Heading>
            <Text fontSize="sm" color="gray.500">
              IP: {ip}
            </Text>

            {relatedCves.length > 0 ? (
              <Box mt={3}>
                <Heading size="sm">関連する脆弱性</Heading>
                <List>
                  {relatedCves.map((cveInfo: CVEInfo, index: number) => (
                    <ListItem key={index}>
                      <Text>
                        <strong>CVE ID:</strong> {cveInfo.id}
                      </Text>
                      <Text>
                        <strong>概要:</strong> {cveInfo.summary}
                      </Text>
                      <Text>
                        <strong>スコア:</strong> {cveInfo.cvss} / 10
                      </Text>
                      <Text>
                        <strong>影響:</strong>
                        機密性({cveInfo.impact?.confidentiality || "N/A"}),
                        完全性({cveInfo.impact?.integrity || "N/A"}), 可用性(
                        {cveInfo.impact?.availability || "N/A"})
                      </Text>
                    </ListItem>
                  ))}
                </List>
              </Box>
            ) : (
              <Text mt={3} color="green.500">
                このホストに関連する脆弱性は見つかりませんでした。
              </Text>
            )}
          </Box>
        );
      })}

      {/* CVE情報全体のキーも表示 */}
      {result.cve?.cves && (
        <Box mt={5} p={4} borderWidth="1px" borderRadius="lg">
          <Heading size="md">CVE情報のキー一覧</Heading>
          <List>
            {Object.keys(result.cve.cves).map((key) => (
              <ListItem key={key}>
                <Text>
                  <strong>キー:</strong> {key}
                </Text>
              </ListItem>
            ))}
          </List>
        </Box>
      )}
    </Box>
  );
};

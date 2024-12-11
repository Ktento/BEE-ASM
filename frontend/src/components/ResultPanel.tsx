import { Box, Heading, List, ListItem, Text } from "@yamada-ui/react";
import { CVEInfo, HostCPEs, HostPorts, Result } from "../types/Restult";

interface Props {
  result: Result;
}

export const ResultPanel = (props: Props) => {
  const { result } = props;
  const hosts = result.subfinder?.hosts || [];
  const hostCpes: HostCPEs = result.nmap?.host_cpes || {};
  const hostPorts: HostPorts = result.nmap?.host_ports || {};
  const hostCpeMapping: Record<string, string[]> = {};
  const hostPortMapping: Record<string, string[]> = {};

  for (const host in hosts) {
    hostCpeMapping[host] = hostCpes[host];
    hostPortMapping[host] = hostPorts[host];
  }

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
      {Object.entries(hosts).map(([host, ip]) => {
        // 該当ホストに関連するCVE, CPE, ポート情報を抽出
        const relatedPorts = hostPortMapping[host];
        const relatedCves = result.cve?.cves?.[host] || [];
        const relatedCpes = hostCpeMapping[host];

        return (
          <Box key={host} mt={5} p={4} borderWidth="1px" borderRadius="lg">
            <Heading size="md">{host}</Heading>
            <Text fontSize="sm" color="gray.500">
              IP: {ip}
            </Text>
            {
              /** ポートの表示 */
              relatedPorts.length > 0 ? (
                <Box mt={3}>
                  <Heading size="sm">解放されているポート</Heading>
                  <List>
                    {relatedPorts.map((port, index) => (
                      <ListItem key={index}>
                        <Text>
                          <strong>PORT:</strong> {port}
                        </Text>
                      </ListItem>
                    ))}
                  </List>
                </Box>
              ) : (
                <Text mt={3} color="green.500">
                  このホストが解放しているポートは見つかりませんでした。
                </Text>
              )
            }

            {
              /** CPEsの表示 */
              relatedCpes.length > 0 ? (
                <Box mt={3}>
                  <Heading size="sm">関連するCPE</Heading>
                  <List>
                    {relatedCpes.map((cpe, index) => (
                      <ListItem key={index}>
                        <Text>
                          <strong>CPE:</strong> {cpe}
                        </Text>
                      </ListItem>
                    ))}
                  </List>
                </Box>
              ) : (
                <Text mt={3} color="green.500">
                  このホストに関連するCPEは見つかりませんでした。
                </Text>
              )
            }
            {
              /** CVEsの表示 */
              relatedCves.length > 0 ? (
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
              )
            }
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

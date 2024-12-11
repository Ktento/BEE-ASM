import { Box, Heading, List, ListItem, Text } from "@yamada-ui/react";
import { HostCPEs, HostPorts, Result } from "../types/Restult";

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

  if (!hosts) {
    return <Heading>ホスト情報が見つかりません。</Heading>;
  }

  return (
    <>
      <Heading>ホストごとの脆弱性</Heading>
      {Object.entries(hosts).map(([host, ip]) => {
        const relatedPorts = hostPortMapping[host];
        const relatedCpes = hostCpeMapping[host];

        return (
          <Box key={host} m={2} p={4} borderWidth="1px" borderRadius="lg">
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
                        <Text>・ {port}</Text>
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
                        <Text>・ CPE: {cpe}</Text>
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
          </Box>
        );
      })}

      {/* CVE情報全体のキーも表示 */}
      {result.cve?.cves && (
        <Box m={2} p={4} borderWidth="1px" borderRadius="lg">
          <Heading size="md">CVE情報のキー一覧</Heading>
          <List>
            {Object.keys(result.cve.cves).map((key) => (
              <ListItem key={key}>
                <Text>・ {key}</Text>
              </ListItem>
            ))}
          </List>
        </Box>
      )}
    </>
  );
};

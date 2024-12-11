import { useState, useEffect, useMemo } from "react";
import {
  Box,
  CircleProgress,
  Heading,
  List,
  ListItem,
  Text,
} from "@yamada-ui/react";
import { HostCPEs, HostInfo, HostPorts, Result } from "../types/Restult";
import { Link } from "react-router-dom";

interface Props {
  result: Result;
}

export const ResultPanel = (props: Props) => {
  const { result } = props;
  const [loading, setLoading] = useState(true);

  const hosts: HostInfo = result.subfinder?.hosts || {};

  const { hostCpeMapping, hostPortMapping } = useMemo(() => {
    const hosts = result.subfinder?.hosts || {};
    const hostCpes: HostCPEs = result.nmap?.host_cpes || {};
    const hostPorts: HostPorts = result.nmap?.host_ports || {};

    const cpeMapping: Record<string, string[]> = {};
    const portMapping: Record<string, string[]> = {};
    for (const host in hosts) {
      cpeMapping[host] = hostCpes[host] || [];
      portMapping[host] = hostPorts[host] || [];
    }
    return { hostCpeMapping: cpeMapping, hostPortMapping: portMapping };
  }, [
    result.subfinder?.hosts,
    result.nmap?.host_cpes,
    result.nmap?.host_ports,
  ]);

  useEffect(() => {
    setLoading(false);
  }, [hostCpeMapping, hostPortMapping]);

  if (!Object.keys(hosts).length) {
    return <Heading>ホスト情報が見つかりません。</Heading>;
  }

  if (loading) {
    return (
      <Box
        display="flex"
        alignItems="center"
        justifyContent="center"
        height="300px"
      >
        <Text>処理中です。</Text>
        <CircleProgress value={18} isAnimation />
      </Box>
    );
  }

  return (
    <>
      <Heading>ホストごとの脆弱性</Heading>
      {Object.entries(hosts).map(([host, ip]) => {
        const relatedPorts = hostPortMapping[host];
        const relatedCpes = hostCpeMapping[host];

        return (
          <Link
            to={`/detail`}
            state={{
              cves: result.cve?.cves,
              host: host,
              cpes: relatedCpes,
            }}
            key={host}
          >
            <Box key={host} m={2} p={4} borderWidth="1px" borderRadius="lg">
              <Heading size="md">{host}</Heading>
              <Text fontSize="sm" color="gray.500">
                IP: {ip}
              </Text>
              {relatedPorts.length > 0 ? (
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
              )}

              {relatedCpes.length > 0 ? (
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
              )}
            </Box>
          </Link>
        );
      })}

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

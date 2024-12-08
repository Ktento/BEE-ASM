import { Box, Button, Heading, Text } from "@yamada-ui/react";
import ConfigPanel from "../components/ConfigPanel";
import { useNavigate } from "react-router-dom";
import { useState } from "react";
import { Config } from "../types/Config";
import { CreateSessionRes } from "../types/CreateSessionReq";
import { SearchRegion } from "../types/enums/SearchRegion";

function Index() {
  const [error, setError] = useState<string | null>(null);
  const [config, setConfig] = useState<Config>({
    target_hosts: [""],
    exclude_hosts: [""],
    color_output: true,
    log_level: "",
    enable_subfinder: true,
    enable_reporting: true,
    report_emails: [""],
    report_limit: 0,
    report_since: "1970-01-01T00:00:00",
    report_min_cvss3: 0,
    report_csv_encoding: "",
    report_enable_gemini: true,
    report_api_key: "",
    report_enable_bcc: true,
    report_from: "",
    enable_nmap: true,
    nmap_extra_args: [],
    search_web: true,
    web_query: "",
    web_region: SearchRegion.JP,
    web_max_results: 0,
    web_backend: "",
    search_cve: true,
  });
  const navigate = useNavigate();
  const ENDPOINT: string = import.meta.env.VITE_END_POINT;

  // バリデーション関数
  const validateConfig = (config: Config): boolean => {
    if (!config.target_hosts.some((host) => host.trim() !== "")) {
      setError("対象ホスト名は少なくとも1つ指定してください。");
      return false;
    }
    setError(null);
    return true;
  };

  const handleSubmit = async (e: React.ChangeEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!validateConfig(config)) {
      return;
    }

    try {
      const header = new Headers();
      header.append("Content-Type", "application/json");

      const res = await fetch(`${ENDPOINT}/session/create`, {
        method: "POST",
        headers: header,
        body: JSON.stringify(config),
      });

      if (!res.ok) return;

      const data: CreateSessionRes = await res.json();
      const sessionId = data.session_id;
      console.log(sessionId);

      const exeRes = await fetch(
        `${ENDPOINT}/asm/execute?session_id=${sessionId}`,
        {
          method: "POST",
          headers: header,
        }
      );

      if (!exeRes.ok) {
        console.log("実行エラー");
        return;
      }

      navigate("/success", { state: { sessionId } });
    } catch (e) {
      console.log(e);
    }
  };

  return (
    <Box as={"main"} p={5}>
      <Heading>ASM Tool</Heading>
      <Box as={"div"} p={5}>
        <form onSubmit={handleSubmit}>
          <ConfigPanel config={config} setConfig={setConfig} />

          {error && (
            <Text color="red.500" mb={4}>
              {error}
            </Text>
          )}

          <Box display={"flex"} justifyContent={"end"}>
            <Button type="submit" colorScheme="purple" variant="outline">
              実行
            </Button>
          </Box>
        </form>
      </Box>
    </Box>
  );
}

export default Index;

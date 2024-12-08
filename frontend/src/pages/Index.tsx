import { Box, Button, Heading } from "@yamada-ui/react";
import ConfigPanel from "../components/ConfigPanel";
import { useNavigate } from "react-router-dom";
import { useState } from "react";
import { Config } from "../types/Config";
import { CreateSessionRes } from "../types/CreateSessionReq";

function Index() {
  const [config, setConfig] = useState<Config>({
    target_hosts: [""],
    exclude_hosts: [""],
    color_output: false,
    log_level: "",
    enable_subfinder: false,
    enable_reporting: false,
    report_emails: [],
    report_limit: 0,
    report_since: "1970-01-01T00:00:00",
    report_min_cvss3: 0,
    report_csv_encoding: "",
    report_enable_gemini: false,
    report_api_key: "",
    report_enable_bcc: false,
    report_from: "",
    enable_nmap: false,
    nmap_extra_args: [],
    search_web: false,
    web_query: "",
    web_region: "",
    web_max_results: 0,
    web_backend: "",
    search_cve: false,
  });
  const navigate = useNavigate();
  const ENDPOINT: string = import.meta.env.VITE_END_POINT;

  const handleSubmit = async (e: React.ChangeEvent<HTMLFormElement>) => {
    e.preventDefault();
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

      const exeRes = await fetch(`${ENDPOINT}/asm/execute`, {
        method: "POST",
        headers: header,
        body: JSON.stringify({
          session_id: sessionId,
        }),
      });

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

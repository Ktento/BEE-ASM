import { Box, Button, Heading } from "@yamada-ui/react";
import ConfigPanel from "../components/ConfigPanel";
import { useNavigate } from "react-router-dom";
import { useState } from "react";
import { Config } from "../types/enums/domain/config";
import { CreateSessionReq } from "../types/enums/CreateSessionReq";

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

  const handleSubmit = async (e: React.ChangeEvent<HTMLFormElement>) => {
    e.preventDefault();
    try {
      const header = new Headers();
      header.append("Content-Type", "application/json");

      const res = await fetch("http://localhost:8000/session/create", {
        method: "POST",
        headers: header,
        body: JSON.stringify(config),
      });

      if (res.ok) {
        const data: CreateSessionReq = await res.json();
        const sessionId = data.session_id;
        console.log(sessionId);

        navigate("/success", { state: { sessionId } });
      } else {
        console.log("failed create session");
      }
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

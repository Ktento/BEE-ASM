import { Accordion, AccordionItem, Box } from "@yamada-ui/react";
import { Config } from "../types/Config";
import { GeneralSettings } from "./settings/GeneralSettings";
import { ReportSettings } from "./settings/ReportSettings";
import { WebSearchSettings } from "./settings/WebSearchSettings";
import { SubfinderSettings } from "./settings/SubfinderSettings";
import { GeminiSettings } from "./settings/GeminiSettings";
import { NmapSettings } from "./settings/NmapSettings";
import { CveSearchSettings } from "./settings/CveSearchSettings";

export interface SettingProps {
  config: Config;
  setConfig: React.Dispatch<React.SetStateAction<Config>>;
}

function ConfigPanel(props: SettingProps) {
  return (
    <Box py={4}>
      <Accordion multiple={true}>
        <AccordionItem label="全体設定">
          <GeneralSettings config={props.config} setConfig={props.setConfig} />
        </AccordionItem>
        <AccordionItem label="subfinder設定">
          <SubfinderSettings
            config={props.config}
            setConfig={props.setConfig}
          />
        </AccordionItem>
        <AccordionItem label="レポート設定">
          <ReportSettings config={props.config} setConfig={props.setConfig} />
        </AccordionItem>
        <AccordionItem label="Gemini設定">
          <GeminiSettings config={props.config} setConfig={props.setConfig} />
        </AccordionItem>
        <AccordionItem label="Nmap設定">
          <NmapSettings config={props.config} setConfig={props.setConfig} />
        </AccordionItem>
        <AccordionItem label="Web検索設定">
          <WebSearchSettings
            config={props.config}
            setConfig={props.setConfig}
          />
        </AccordionItem>
        <AccordionItem label="CVE検索設定">
          <CveSearchSettings
            config={props.config}
            setConfig={props.setConfig}
          />
        </AccordionItem>
      </Accordion>
    </Box>
  );
}

export default ConfigPanel;

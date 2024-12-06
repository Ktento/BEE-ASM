import {
  Accordion,
  AccordionItem,
  Box,
  Checkbox,
  FormControl,
  Input,
  Radio,
  RadioGroup,
} from "@yamada-ui/react";
import { useState } from "react";
import { SearchRegion } from "../types/enums/SearchRegion";
import ConfigCard from "./ConfigCard";
import { Config } from "../types/enums/domain/config";

function ConfigPanel() {
  const [config, setConfig] = useState<Config>({
    target_hosts: [], // TODO
    exclude_hosts: [], // TODO
    color_output: false,
    log_level: "", // TODO
    enable_subfinder: false,
    enable_reporting: false,
    report_emails: [],
    report_limit: 0,
    report_since: "",
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

  return (
    <Box py={4}>
      <Accordion multiple={true}>
        <AccordionItem label="全体設定">
          <FormControl label="対象ホスト名" py={5}>
            <Input
              placeholder="domain"
              value={config.target_hosts}
              onChange={() => setConfig({ ...config })} // TODO: 配列化
              width={"70%"}
            />
          </FormControl>
          <FormControl label="除外ホスト名" py={5}>
            <Input
              placeholder="exclude_hosts"
              value={config.exclude_hosts}
              onChange={() => setConfig({ ...config })} // TODO: 配列化
              width={"70%"}
            />
          </FormControl>
          <ConfigCard
            content={
              <Checkbox
                isChecked={config.color_output}
                onChange={(e) =>
                  setConfig({ ...config, color_output: e.target.checked })
                }
              >
                標準出力の色付けを有効にしますか?
              </Checkbox>
            }
          />
        </AccordionItem>
        <AccordionItem label="subfinder設定">
          <ConfigCard
            content={
              <Checkbox
                isChecked={config.enable_subfinder}
                onChange={(e) =>
                  setConfig({ ...config, enable_subfinder: e.target.checked })
                }
              >
                subfinderを使用しますか?
              </Checkbox>
            }
          />
        </AccordionItem>
        <AccordionItem label="レポート設定">
          <ConfigCard
            content={
              <>
                <Checkbox
                  isChecked={config.enable_reporting}
                  onChange={(e) =>
                    setConfig({ ...config, enable_reporting: e.target.checked })
                  }
                >
                  レポート機能を利用しますか?
                </Checkbox>
                {config.enable_reporting && (
                  <Box px={8}>
                    <FormControl label="調査開始期間">
                      <Input
                        type="since"
                        placeholder="1970-01-01T00:00:00"
                        value={config.report_since}
                        onChange={(e) =>
                          setConfig({
                            ...config,
                            report_since: e.target.value,
                          })
                        }
                        width={"auto"}
                      />
                    </FormControl>
                    <Checkbox
                      isChecked={config.report_enable_bcc}
                      onChange={(e) =>
                        setConfig({
                          ...config,
                          report_enable_bcc: e.target.checked,
                        })
                      }
                    >
                      CCの代わりにBCCを使用しますか？
                    </Checkbox>
                    <FormControl label="レポート送信先メールアドレス">
                      <Input
                        type="email"
                        placeholder="email"
                        value={config.report_emails}
                        onChange={() =>
                          setConfig({
                            ...config, // TODO: 配列化
                          })
                        }
                        width={"auto"}
                      />
                    </FormControl>
                    <FormControl label="Geminiにレビューさせる件数">
                      <Input
                        type="件数"
                        value={config.report_limit}
                        onChange={(e) =>
                          setConfig({
                            ...config,
                            report_limit: parseInt(e.target.value),
                          })
                        }
                        width={"auto"}
                      />
                    </FormControl>
                  </Box>
                )}
              </>
            }
          />
        </AccordionItem>
        <AccordionItem label="Gemini設定">
          <ConfigCard
            content={
              <>
                <Checkbox
                  isChecked={config.report_enable_gemini}
                  onChange={(e) =>
                    setConfig({
                      ...config,
                      report_enable_gemini: e.target.checked,
                    })
                  }
                >
                  Geminiによる分析を使用しますか?
                </Checkbox>
              </>
            }
          />
        </AccordionItem>
        <AccordionItem label="Nmap設定">
          <ConfigCard
            content={
              <>
                <Checkbox
                  isChecked={config.enable_nmap}
                  onChange={(e) =>
                    setConfig({ ...config, enable_nmap: e.target.checked })
                  }
                >
                  Nmapを使用しますか?
                </Checkbox>
                {config.enable_nmap && (
                  <Box px={8}>
                    <FormControl label="Nmapの引数">
                      <Input
                        type="text"
                        placeholder="nmap arguments"
                        value={config.nmap_extra_args}
                        onChange={() =>
                          setConfig({
                            ...config,
                            // TODO: 配列化
                          })
                        }
                        width={"auto"}
                      />
                    </FormControl>
                  </Box>
                )}
              </>
            }
          />
        </AccordionItem>
        <AccordionItem label="Web検索設定">
          <ConfigCard
            content={
              <>
                <Checkbox
                  isChecked={config.search_web}
                  onChange={(e) =>
                    setConfig({ ...config, search_web: e.target.checked })
                  }
                >
                  Web検索機能を使用しますか?
                </Checkbox>
                {config.search_web && (
                  <Box px={8}>
                    <FormControl label="検索クエリ">
                      <Input
                        type="text"
                        placeholder="search query"
                        value={config.web_query}
                        onChange={(e) =>
                          setConfig({
                            ...config,
                            web_query: e.target.value,
                          })
                        }
                        width={"auto"}
                      />
                    </FormControl>
                    <RadioGroup
                      value={config.web_region}
                      onChange={() => setConfig({ ...config })} // TODO: set region
                    >
                      <Radio value={SearchRegion.JP}>日本</Radio>
                    </RadioGroup>
                    <FormControl label="検索上限">
                      <Input
                        type="number"
                        placeholder="max results"
                        value={config.web_max_results}
                        onChange={(e) =>
                          setConfig({
                            ...config,
                            web_max_results: parseInt(e.target.value),
                          })
                        }
                        width={"auto"}
                      />
                    </FormControl>
                    <FormControl label="検索バックエンド">
                      <Input
                        type="text"
                        placeholder="web backend"
                        value={config.web_backend}
                        onChange={(e) =>
                          setConfig({ ...config, web_backend: e.target.value })
                        }
                        width={"auto"}
                      />
                    </FormControl>
                  </Box>
                )}
              </>
            }
          />
        </AccordionItem>
        <AccordionItem label="CVE検索設定">
          <ConfigCard
            content={
              <Checkbox
                isChecked={config.search_cve}
                onChange={(e) =>
                  setConfig({ ...config, search_cve: e.target.checked })
                }
              >
                CVE検索機能を使用しますか?
              </Checkbox>
            }
          />
        </AccordionItem>
      </Accordion>
    </Box>
  );
}

export default ConfigPanel;

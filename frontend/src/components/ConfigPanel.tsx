import {
  Accordion,
  AccordionItem,
  Box,
  Button,
  Checkbox,
  FormControl,
  Input,
  Radio,
  RadioGroup,
} from "@yamada-ui/react";
import { SearchRegion } from "../types/enums/SearchRegion";
import ConfigCard from "./ConfigCard";
import { Config } from "../types/Config";

interface Props {
  config: Config;
  setConfig: React.Dispatch<React.SetStateAction<Config>>;
}

function ConfigPanel(props: Props) {
  const handleAddTargetHost = () => {
    props.setConfig({
      ...props.config,
      target_hosts: [...props.config.target_hosts, ""],
    });
  };

  const handleChangeTargetHost = (index: number, value: string) => {
    const newHosts = [...props.config.target_hosts];
    newHosts[index] = value;
    props.setConfig({ ...props.config, target_hosts: newHosts });
  };

  const handleAddExcludeHost = () => {
    props.setConfig({
      ...props.config,
      exclude_hosts: [...props.config.exclude_hosts, ""],
    });
  };

  const handleChangeExcludeHost = (index: number, value: string) => {
    const newHosts = [...props.config.exclude_hosts];
    newHosts[index] = value;
    props.setConfig({ ...props.config, exclude_hosts: newHosts });
  };

  return (
    <Box py={4}>
      <Accordion multiple={true}>
        <AccordionItem label="全体設定">
          <FormControl label="対象ホスト名" py={5}>
            {props.config.target_hosts.map((host, index) => (
              <Box key={index} alignItems={"center"} mb={2}>
                <Input
                  placeholder="domain"
                  value={host}
                  onChange={(e) =>
                    handleChangeTargetHost(index, e.target.value)
                  }
                  width={"70%"}
                />
              </Box>
            ))}
            <Button onClick={handleAddTargetHost}>+</Button>
          </FormControl>
          <FormControl label="除外ホスト名" py={5}>
            {props.config.exclude_hosts.map((host, index) => (
              <Box key={index} display="flex" alignItems="center" mb={2}>
                <Input
                  placeholder="exclude_hosts"
                  value={host}
                  onChange={(e) =>
                    handleChangeExcludeHost(index, e.target.value)
                  }
                  width={"70%"}
                  mr={2}
                />
              </Box>
            ))}
            <Button onClick={handleAddExcludeHost}>+</Button>
          </FormControl>
          <ConfigCard
            content={
              <Checkbox
                isChecked={props.config.color_output}
                onChange={(e) =>
                  props.setConfig({
                    ...props.config,
                    color_output: e.target.checked,
                  })
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
                isChecked={props.config.enable_subfinder}
                onChange={(e) =>
                  props.setConfig({
                    ...props.config,
                    enable_subfinder: e.target.checked,
                  })
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
                  isChecked={props.config.enable_reporting}
                  onChange={(e) =>
                    props.setConfig({
                      ...props.config,
                      enable_reporting: e.target.checked,
                    })
                  }
                >
                  レポート機能を利用しますか?
                </Checkbox>
                {props.config.enable_reporting && (
                  <Box px={8}>
                    <FormControl label="調査開始期間">
                      <Input
                        type="since"
                        placeholder="1970-01-01T00:00:00"
                        value={props.config.report_since}
                        onChange={(e) =>
                          props.setConfig({
                            ...props.config,
                            report_since: e.target.value,
                          })
                        }
                        width={"auto"}
                      />
                    </FormControl>
                    <Checkbox
                      isChecked={props.config.report_enable_bcc}
                      onChange={(e) =>
                        props.setConfig({
                          ...props.config,
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
                        value={props.config.report_emails}
                        onChange={() =>
                          props.setConfig({
                            ...props.config, // TODO: 配列化
                          })
                        }
                        width={"auto"}
                      />
                    </FormControl>
                    <FormControl label="Geminiにレビューさせる件数">
                      <Input
                        type="件数"
                        value={props.config.report_limit}
                        onChange={(e) =>
                          props.setConfig({
                            ...props.config,
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
                  isChecked={props.config.report_enable_gemini}
                  onChange={(e) =>
                    props.setConfig({
                      ...props.config,
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
                  isChecked={props.config.enable_nmap}
                  onChange={(e) =>
                    props.setConfig({
                      ...props.config,
                      enable_nmap: e.target.checked,
                    })
                  }
                >
                  Nmapを使用しますか?
                </Checkbox>
                {props.config.enable_nmap && (
                  <Box px={8}>
                    <FormControl label="Nmapの引数">
                      <Input
                        type="text"
                        placeholder="nmap arguments"
                        value={props.config.nmap_extra_args}
                        onChange={() =>
                          props.setConfig({
                            ...props.config,
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
                  isChecked={props.config.search_web}
                  onChange={(e) =>
                    props.setConfig({
                      ...props.config,
                      search_web: e.target.checked,
                    })
                  }
                >
                  Web検索機能を使用しますか?
                </Checkbox>
                {props.config.search_web && (
                  <Box px={8}>
                    <FormControl label="検索クエリ">
                      <Input
                        type="text"
                        placeholder="search query"
                        value={props.config.web_query}
                        onChange={(e) =>
                          props.setConfig({
                            ...props.config,
                            web_query: e.target.value,
                          })
                        }
                        width={"auto"}
                      />
                    </FormControl>
                    <RadioGroup
                      value={props.config.web_region}
                      onChange={() => props.setConfig({ ...props.config })} // TODO: set region
                    >
                      <Radio value={SearchRegion.JP}>日本</Radio>
                    </RadioGroup>
                    <FormControl label="検索上限">
                      <Input
                        type="number"
                        placeholder="max results"
                        value={props.config.web_max_results}
                        onChange={(e) =>
                          props.setConfig({
                            ...props.config,
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
                        value={props.config.web_backend}
                        onChange={(e) =>
                          props.setConfig({
                            ...props.config,
                            web_backend: e.target.value,
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
        <AccordionItem label="CVE検索設定">
          <ConfigCard
            content={
              <Checkbox
                isChecked={props.config.search_cve}
                onChange={(e) =>
                  props.setConfig({
                    ...props.config,
                    search_cve: e.target.checked,
                  })
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

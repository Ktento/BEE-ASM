import {
  Accordion,
  AccordionItem,
  Box,
  Card,
  CardBody,
  CardHeader,
  Checkbox,
  FormControl,
  Heading,
  Input,
  Radio,
  RadioGroup,
} from "@yamada-ui/react";
import { useState } from "react";
import { SearchRegion } from "../types/enums/SearchRegion";

function Config() {
  const [enableColor, setEnableColor] = useState(false);
  const [enableSubfinder, setEnableSubfinder] = useState(false);
  const [enableReporting, setEnableReporting] = useState(false);
  const [enableBCC, setEnableBCC] = useState(false);
  const [email, setEmail] = useState<string | undefined>(undefined);
  const [enableGemini, setEnableGemini] = useState(false);
  const [geminiAPIKey, setGeminiAPIKey] = useState<string | undefined>(
    undefined
  );
  const [enableNmap, setEnableNmap] = useState(false);
  const [nmapArgs, setNmapArgs] = useState<string | undefined>(undefined);
  const [enableWebSearch, setEnableWebSearch] = useState(false);
  const [webQuery, setWebQuery] = useState<string | undefined>(undefined);
  const [selectedRegion, setSelectedRegion] = useState<SearchRegion>(
    SearchRegion.JP
  );
  const [webMaxResults, setWebMaxResults] = useState(50);
  const [webBackend, setWebBackend] = useState("html");
  const [enableSearchCVE, setEnableSearchCVE] = useState(false);
  const [enableVAT, setEnableVAT] = useState(false);

  return (
    <>
      <Accordion multiple={true}>
        <AccordionItem label="全体設定">
          <ConfigCard
            content={
              <Checkbox
                isChecked={enableColor}
                onChange={(e) => setEnableColor(e.target.checked)}
              >
                標準出力の色付けを有効にしますか?
              </Checkbox>
            }
          />
          {/**
           * 追加するもの
           * 除外するホストやネットワーク範囲
           * 出力するログのレベル
           */}
        </AccordionItem>
        <AccordionItem label="subfinder設定">
          <ConfigCard
            content={
              <Checkbox
                isChecked={enableSubfinder}
                onChange={(e) => setEnableSubfinder(e.target.checked)}
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
                  isChecked={enableReporting}
                  onChange={(e) => setEnableReporting(e.target.checked)}
                >
                  レポート機能を利用しますか?
                </Checkbox>
                {enableReporting && (
                  <Box px={8}>
                    <Checkbox
                      isChecked={enableBCC}
                      onChange={(e) => setEnableBCC(e.target.checked)}
                    >
                      CCの代わりにBCCを使用しますか？
                    </Checkbox>
                    <FormControl label="レポート送信先メールアドレス">
                      <Input
                        type="email"
                        placeholder="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
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
                  isChecked={enableGemini}
                  onChange={(e) => setEnableGemini(e.target.checked)}
                >
                  Geminiによる分析を使用しますか?
                </Checkbox>
                {enableGemini && (
                  <Box px={8}>
                    <FormControl label="GeminiのAPIキー">
                      <Input
                        type="text"
                        placeholder="Gemini API key"
                        value={geminiAPIKey}
                        onChange={(e) => setGeminiAPIKey(e.target.value)}
                        width={"auto"}
                      />
                    </FormControl>
                  </Box>
                )}
              </>
            }
          />
        </AccordionItem>
        <AccordionItem label="Nmap設定">
          <ConfigCard
            content={
              <>
                <Checkbox
                  isChecked={enableNmap}
                  onChange={(e) => setEnableNmap(e.target.checked)}
                >
                  Nmapを使用しますか?
                </Checkbox>
                {enableNmap && (
                  <Box px={8}>
                    <FormControl label="Nmapの引数">
                      <Input
                        type="text"
                        placeholder="nmap arguments"
                        value={nmapArgs}
                        onChange={(e) => setNmapArgs(e.target.value)}
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
                  isChecked={enableWebSearch}
                  onChange={(e) => setEnableWebSearch(e.target.checked)}
                >
                  Web検索機能を使用しますか?
                </Checkbox>
                {enableWebSearch && (
                  <Box px={8}>
                    <FormControl label="検索クエリ">
                      <Input
                        type="text"
                        placeholder="search query"
                        value={webQuery}
                        onChange={(e) => setWebQuery(e.target.value)}
                        width={"auto"}
                      />
                    </FormControl>
                    <RadioGroup
                      value={selectedRegion}
                      onChange={(e) => setSelectedRegion(e as SearchRegion)}
                    >
                      <Radio value={SearchRegion.JP}>日本</Radio>
                    </RadioGroup>
                    <FormControl label="検索上限">
                      <Input
                        type="number"
                        placeholder="max results"
                        value={webMaxResults}
                        onChange={(e) =>
                          setWebMaxResults(parseInt(e.target.value))
                        }
                        width={"auto"}
                      />
                    </FormControl>
                    <FormControl label="検索バックエンド">
                      <Input
                        type="text"
                        placeholder="web backend"
                        value={webBackend}
                        onChange={(e) => setWebBackend(e.target.value)}
                        width={"auto"}
                      />
                    </FormControl>
                  </Box>
                )}
                <AccordionItem label="CVE検索設定">
                  <ConfigCard
                    content={
                      <Checkbox
                        isChecked={enableSearchCVE}
                        onChange={(e) => setEnableSearchCVE(e.target.checked)}
                      >
                        CVE検索機能を使用しますか?
                      </Checkbox>
                    }
                  />
                </AccordionItem>
                <AccordionItem label="脆弱性診断設定">
                  <ConfigCard
                    content={
                      <Checkbox
                        isChecked={enableVAT}
                        onChange={(e) => setEnableVAT(e.target.checked)}
                      >
                        脆弱性診断を使用しますか?
                      </Checkbox>
                    }
                  />
                </AccordionItem>
              </>
            }
          />
        </AccordionItem>
      </Accordion>
    </>
  );
}

interface ConfigCardProps {
  header?: string;
  content: JSX.Element;
}

function ConfigCard(props: ConfigCardProps) {
  return (
    <Card>
      {props.header && (
        <CardHeader>
          <Heading>{props.header}</Heading>
        </CardHeader>
      )}
      <CardBody>{props.content}</CardBody>
    </Card>
  );
}
export default Config;

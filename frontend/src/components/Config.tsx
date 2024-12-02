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
} from "@yamada-ui/react";
import { useState } from "react";

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
                  <Box>
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

import {
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
  const [email, setEmail] = useState("");

  return (
    <>
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
              <>
                <Checkbox
                  isChecked={enableBCC}
                  onChange={(e) => setEnableBCC(e.target.checked)}
                >
                  CCの代わりにBCCを使用しますか？
                </Checkbox>
                <FormControl label="レポート送信先メールアドレス">
                  <Input
                    placeholder="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    width={"65%"}
                  ></Input>
                </FormControl>
              </>
            )}
          </>
        }
      />
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

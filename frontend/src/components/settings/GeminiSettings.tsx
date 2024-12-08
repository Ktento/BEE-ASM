import { Checkbox } from "@yamada-ui/react";
import ConfigCard from "../ConfigCard";
import { SettingProps } from "../ConfigPanel";

export const GeminiSettings = (props: SettingProps) => {
  return (
    <ConfigCard
      content={
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
      }
    />
  );
};

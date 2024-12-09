import { Checkbox } from "@yamada-ui/react";
import ConfigCard from "../ConfigCard";
import { SettingProps } from "../ConfigPanel";

export const CveSearchSettings = (props: SettingProps) => {
  return (
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
  );
};

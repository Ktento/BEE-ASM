import { Checkbox } from "@yamada-ui/react";
import { SettingProps } from "../ConfigPanel";

export const NmapSettings = (props: SettingProps) => {
  return (
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
  );
};

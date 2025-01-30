import { Checkbox } from "@yamada-ui/react";
import { SettingProps } from "../ConfigPanel";

export const SubfinderSettings = (props: SettingProps) => {
  return (
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
  );
};

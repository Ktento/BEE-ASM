import { Box, Checkbox, FormControl, Input } from "@yamada-ui/react";
import ConfigCard from "../ConfigCard";
import { SettingProps } from "../ConfigPanel";

export const NmapSettings = (props: SettingProps) => {
  return (
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
  );
};

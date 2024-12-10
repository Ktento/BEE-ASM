import { Box, Button, Checkbox, FormControl, Input } from "@yamada-ui/react";
import { SettingProps } from "../ConfigPanel";

export const GeneralSettings = (props: SettingProps) => {
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
  const handleAddTargetHost = () => {
    props.setConfig({
      ...props.config,
      target_hosts: [...props.config.target_hosts, ""],
    });
  };

  return (
    <>
      <FormControl label="対象ホスト名" py={5}>
        {props.config.target_hosts.map((host, index) => (
          <Box key={index} alignItems={"center"} mb={2}>
            <Input
              placeholder="domain"
              value={host}
              onChange={(e) => handleChangeTargetHost(index, e.target.value)}
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
              onChange={(e) => handleChangeExcludeHost(index, e.target.value)}
              mr={2}
            />
          </Box>
        ))}
        <Button onClick={handleAddExcludeHost}>+</Button>
      </FormControl>

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
    </>
  );
};

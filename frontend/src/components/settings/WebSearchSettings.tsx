import {
  Box,
  Checkbox,
  FormControl,
  Input,
  Radio,
  RadioGroup,
} from "@yamada-ui/react";
import { SettingProps } from "../ConfigPanel";
import { SearchRegion } from "../../types/enums/SearchRegion";

export const WebSearchSettings = (props: SettingProps) => {
  return (
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
        <Box>
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
            />
          </FormControl>
          <RadioGroup
            value={props.config.web_region}
            onChange={(value: SearchRegion) =>
              props.setConfig({
                ...props.config,
                web_region: value,
              })
            }
          >
            <Radio value={SearchRegion.JP}>日本</Radio>
            <Radio value={SearchRegion.US}>アメリカ</Radio>
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
            />
          </FormControl>
        </Box>
      )}
    </>
  );
};

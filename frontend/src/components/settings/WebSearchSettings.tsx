import {
  Box,
  Checkbox,
  FormControl,
  Input,
  Radio,
  RadioGroup,
} from "@yamada-ui/react";
import ConfigCard from "../ConfigCard";
import { SettingProps } from "../ConfigPanel";
import { SearchRegion } from "../../types/enums/SearchRegion";

export const WebSearchSettings = (props: SettingProps) => {
  return (
    <>
      <ConfigCard
        content={
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
              <Box px={8}>
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
                    width={"auto"}
                  />
                </FormControl>
                <RadioGroup
                  value={props.config.web_region}
                  onChange={() => props.setConfig({ ...props.config })} // TODO: set region
                >
                  <Radio value={SearchRegion.JP}>日本</Radio>
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
                    width={"auto"}
                  />
                </FormControl>
                <FormControl label="検索バックエンド">
                  <Input
                    type="text"
                    placeholder="web backend"
                    value={props.config.web_backend}
                    onChange={(e) =>
                      props.setConfig({
                        ...props.config,
                        web_backend: e.target.value,
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
    </>
  );
};

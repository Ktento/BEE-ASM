import { useState } from "react";
import ConfigCard from "../ConfigCard";
import { Box, Checkbox, FormControl, Input, Text } from "@yamada-ui/react";
import { SettingProps } from "../ConfigPanel";

export const ReportSettings = (props: SettingProps) => {
  const [year, setYear] = useState(props.config.report_since.slice(0, 4));
  const [month, setMonth] = useState(props.config.report_since.slice(5, 7));
  const [day, setDay] = useState(props.config.report_since.slice(8, 10));

  // 入力が変更されるたびにISO形式の日付を再構成して反映
  const handleDateChange = (type: "year" | "month" | "day", value: string) => {
    const updatedYear = type === "year" ? value : year;
    const updatedMonth = type === "month" ? value.padStart(2, "0") : month;
    const updatedDay = type === "day" ? value.padStart(2, "0") : day;

    setYear(updatedYear);
    setMonth(updatedMonth);
    setDay(updatedDay);

    const newDate = `${updatedYear}-${updatedMonth}-${updatedDay}T00:00:00`;
    props.setConfig({ ...props.config, report_since: newDate });
  };

  return (
    <>
      <ConfigCard
        content={
          <>
            <Checkbox
              isChecked={props.config.enable_reporting}
              onChange={(e) =>
                props.setConfig({
                  ...props.config,
                  enable_reporting: e.target.checked,
                })
              }
            >
              レポート機能を利用しますか?
            </Checkbox>
            {props.config.enable_reporting && (
              <Box px={8}>
                <FormControl label="調査開始期間">
                  <Box display="flex" alignItems="center" gap={2}>
                    <Box>
                      <Text>年</Text>
                      <Input
                        type="number"
                        value={year}
                        onChange={(e) =>
                          handleDateChange("year", e.target.value)
                        }
                        width="100px"
                      />
                    </Box>
                    <Box>
                      <Text>月</Text>
                      <Input
                        type="number"
                        value={month}
                        min={1}
                        max={12}
                        onChange={(e) =>
                          handleDateChange("month", e.target.value)
                        }
                        width="70px"
                      />
                    </Box>
                    <Box>
                      <Text>日</Text>
                      <Input
                        type="number"
                        value={day}
                        min={1}
                        max={31}
                        onChange={(e) =>
                          handleDateChange("day", e.target.value)
                        }
                        width="70px"
                      />
                    </Box>
                  </Box>
                </FormControl>
                <Checkbox
                  isChecked={props.config.report_enable_bcc}
                  onChange={(e) =>
                    props.setConfig({
                      ...props.config,
                      report_enable_bcc: e.target.checked,
                    })
                  }
                >
                  CCの代わりにBCCを使用しますか？
                </Checkbox>
                <FormControl label="レポート送信先メールアドレス">
                  <Input
                    type="email"
                    placeholder="email"
                    value={props.config.report_emails}
                    onChange={() =>
                      props.setConfig({
                        ...props.config, // TODO: 配列化
                      })
                    }
                    width={"auto"}
                  />
                </FormControl>
                <FormControl label="Geminiにレビューさせる件数">
                  <Input
                    type="件数"
                    value={props.config.report_limit}
                    onChange={(e) =>
                      props.setConfig({
                        ...props.config,
                        report_limit: parseInt(e.target.value),
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

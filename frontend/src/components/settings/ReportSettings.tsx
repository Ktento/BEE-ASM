import { useState } from "react";
import ConfigCard from "../ConfigCard";
import {
  Box,
  Checkbox,
  FormControl,
  Input,
  Button,
  Text,
} from "@yamada-ui/react";
import { SettingProps } from "../ConfigPanel";

export const ReportSettings = (props: SettingProps) => {
  const [year, setYear] = useState(props.config.report_since.slice(0, 4));
  const [month, setMonth] = useState(props.config.report_since.slice(5, 7));
  const [day, setDay] = useState(props.config.report_since.slice(8, 10));

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

  const handleAddEmail = () => {
    props.setConfig({
      ...props.config,
      report_emails: [...props.config.report_emails, ""],
    });
  };

  const handleChangeEmail = (index: number, value: string) => {
    const newEmails = [...props.config.report_emails];
    newEmails[index] = value;
    props.setConfig({ ...props.config, report_emails: newEmails });
  };

  const handleRemoveEmail = (index: number) => {
    const newEmails = props.config.report_emails.filter((_, i) => i !== index);
    props.setConfig({ ...props.config, report_emails: newEmails });
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
                  {props.config.report_emails.map((email, index) => (
                    <Box key={index} display="flex" alignItems="center" mb={2}>
                      <Input
                        type="email"
                        placeholder="email"
                        value={email}
                        onChange={(e) =>
                          handleChangeEmail(index, e.target.value)
                        }
                        width="70%"
                        mr={2}
                      />
                      <Button onClick={() => handleRemoveEmail(index)}>
                        -
                      </Button>
                    </Box>
                  ))}
                  <Button onClick={handleAddEmail}>+</Button>
                </FormControl>
                <FormControl label="Geminiにレビューさせる件数">
                  <Input
                    type="number"
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

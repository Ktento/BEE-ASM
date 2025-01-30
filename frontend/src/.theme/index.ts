import { extendTheme, UsageTheme } from "@yamada-ui/react";
import { styles } from "./styles";
import { components } from "./components";

const customTheme: UsageTheme = {
  styles,
  components,
};

export const theme = extendTheme(customTheme)();

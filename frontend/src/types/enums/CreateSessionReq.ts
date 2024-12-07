import { Config } from "./domain/config";

export type CreateSessionRes = {
  session_id: string;
  config: Config;
};

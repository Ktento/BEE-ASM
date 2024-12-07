import { Config } from "./domain/config";

export type CreateSessionReq = {
  session_id: string;
  config: Config;
};

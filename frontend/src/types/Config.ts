import { SearchRegion } from "./enums/SearchRegion";

export type Config = {
  // general config
  target_hosts: string[];
  exclude_hosts: string[];
  color_output: boolean;
  log_level: string;

  // subfinder config
  enable_subfinder: boolean;

  // report config
  enable_reporting: boolean;
  report_emails: string[];
  report_limit: number;
  report_since: string;
  report_min_cvss3: number;
  report_csv_encoding: string;
  report_enable_gemini: boolean;
  report_enable_bcc: boolean;
  report_from: string;

  // nmap config
  enable_nmap: boolean;
  nmap_extra_args: string[];

  // web search config
  search_web: boolean;
  web_query: string;
  web_region: SearchRegion;
  web_max_results: number;
  web_backend: string;

  // cve search
  search_cve: boolean;
};

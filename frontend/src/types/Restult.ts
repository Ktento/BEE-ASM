// 主な型定義
export type Result = {
  subfinder?: SubfinderResult;
  nmap?: NmapResult;
  cve?: CveResult;
  web_search?: WebSearchResult;
  report?: ReportResult;
};

export type SubfinderResult = {
  hosts?: HostInfo;
};

export type HostInfo = {
  [key: string]: string; // 各ホスト名とIPアドレスのマッピング
};

export type NmapResult = {
  result?: string;
  stderr?: string; // デバッグ情報やエラーメッセージ
};

export type CveResult = {
  cves?: {
    [key: string]: CVEInfo[]; // 各CPEに関連付けられたCVE情報のリスト
  };
};

export type CVEInfo = {
  refmap?: RefMap;
  vulnerable_configuration?: VulnerableConfiguration[];
  //   vulnerable_configuration_cpe_2_2?: string[]; // 空配列の場合
  vulnerable_product?: string[];
  statements?: Statement[];
  Modified?: string;
  Published?: string;
  access?: CVEAccess;
  assigner?: string;
  cvss?: number;
  impactScore?: number;
  exploitabilityScore?: number;
  cvssTime?: string;
  cvssVector?: string;
  cwe?: string;
  id?: string;
  impact?: CVEImpact;
  lastModified?: string;
  references?: string[];
  summary?: string;
};

export type RefMap = {
  bugtraq?: string[];
  confirm?: string[];
};

export type VulnerableConfiguration = {
  id: string;
  title?: string;
};

export type Statement = {
  contributor?: string;
  lastmodified?: string;
  organization?: string;
  statement?: string;
};

export type CVEAccess = {
  authentication?: string;
  complexity?: string;
  vector?: string;
};

export type CVEImpact = {
  availability?: string;
  confidentiality?: string;
  integrity?: string;
};

export type WebSearchResult = {
  result?: WebSearchItem[];
};

export type WebSearchItem = {
  title: string;
  href: string;
  body: string;
};

export type ReportResult = {
  csv_all?: string;
  csv_per?: string;
  html?: string;
  mail_sent?: boolean;
};

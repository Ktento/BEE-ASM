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
  cve_data?: CVEData[]; // 追加：CVE情報のサブセット
  host_cpes?: HostCPEs; // 追加：ホストと関連するCPE文字列
  host_cpe_ports?: HostCPEPorts[]; // 追加：「ホストとCPEの組」に対応するプロトコルとポート番号の配列
};

export type CVEInfo = {
  refmap?: RefMap;
  vulnerable_configuration?: VulnerableConfiguration[];
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

export type CVEData = {
  cpe: string; // CPE文字列
  id: string; // CVE ID
  published: string; // 公開日時（ISO 8601形式）
  published_str: string; // 公開日時（文字列形式）
  cvss: number; // CVSSスコア
  cvss3: number; // CVSS v3スコア
  summary: string; // 脆弱性の概要
  gemini?: string; // 脆弱性評価の説明や追加情報
};

export type HostCPEs = {
  [host: string]: string[]; // 各ホストと関連付けられたCPE文字列の配列
};

export type HostCPEPorts = {
  host: string; // ホスト名またはIPアドレス
  cpe: string; // CPE文字列
  ports: string[]; // プロトコルとポート番号の配列（例: "tcp/80"）
}[];

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

export type TaskProgresses = {
  subfinder: number;
  nmap: number;
  websearch: number;
  cve: number;
  reporting: number;
  asm: number;
};

export type ProgressesRes = {
  session_id: string;
  started_at: string;
  current_tasks: string[];
  task_progresses: TaskProgresses;
  overall_progress: number;
};

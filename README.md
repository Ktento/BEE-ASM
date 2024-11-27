# ASMツール
サブドメイン探索、Web検索、サービス列挙、CVE情報の取得、Eメール報告などの機能を持つASMツールです。

## 簡単な説明
* 設定ファイル: `config.py`
* 実行方法: `python3 .`

設定を編集してから実行してください。

Eメール報告機能では、CVSS3スコアの高い方から優先的にレポートするようになっています。

## ファイルの説明
### `__main__.py`
メインの実行ファイルです。

### `config.py`
設定ファイルです。
具体的な設定内容については同ファイルを参照してください。

### `log.py`
ロギング関連の関数がまとまっています。

### `context.py`
グローバル変数の代替です。

### `proc_subfinder.py`
subfinderを用いてサブドメインを探す機能を担っています。
サブドメインが見つかった場合、見つかったサブドメインも検査対象に加えます。

### `proc_nmap.py`
Nmapを用いてサービス列挙を行う機能を担っています。

### `proc_cve.py`
Nmapから取得したCPE文字列を用いてCVE情報を取得します。
そのためNmapを実行しないよう設定した場合はこのファイルも実行されません。

### `proc_ddg.py`
DuckDuckGoで検索する機能を担っています。

### `proc_report.py`
CVE情報をGeminiに分析させたり、
Eメールを使用してCVE情報を報告する機能を担っています。

### `vat`
脆弱性診断ツール(VAT)のプレースホルダーです。
実際に脆弱性診断を行う場合、このファイルを診断ツールの実行ファイルで置き換えてください。

### `requirements.txt`
依存関係についてのファイルです。
pipで利用することができます。
```bash
pip3 install -r requirements.txt
```

### `README.md`
あなたが今読んでいる、このファイルです。

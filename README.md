# ASMツール
サブドメイン探索、Web検索、サービス列挙、CVE情報の取得、Eメール報告などの機能を持つASMツールです。

## バックエンド
### 簡単な説明
とりあえず実行したい、そういう場合には以下のように実行してみてください。
1. バックエンドのAPIサーバーの起動
2. 起動したAPIサーバーの`/session/create`で新規セッションの作成
3. `/asm/execute`でASM処理の実行
4. `/progress/show`で進捗状況の確認
5. サーバーのファイルシステムの`work/<セッションID>`配下にある結果ファイルの確認

Eメール報告機能では、CVSS3スコアの高い方から優先的にレポートするようになっています。
CVSS, CVSS3スコアが不明なものは`-1.0`として扱われます。

#### APIサーバーの実行方法
`backend/app/fastapi_main.py`をUvicornで実行してください。

例:
```bash
# 依存関係のインストール
pip3 install -r backend/requirements.txt

# サーバーの実行
cd backend/app/
python3 -m uvicorn fastapi_main:app --port <ポート番号> --reload
```

#### セッションの作成
先程実行したサーバーの`/session/create`宛に`POST`リクエストを発行することでセッションを作成できます。
リクエストボディーはJSON形式で、設定が格納されます。
セッションの作成に成功するとセッション情報のJSONが返されます。このJSONにある`session_id`が後に使うセッションIDとなりますのでご確認ください。

<details>
<summary>設定例</summary>

```json
{
	"target_hosts": ["検査対象のホスト.example.com"],
	"exclude_hosts": [],

	"color_output": true,
	"log_level": "ALL",
	"nmap_extra_args": [],

	"enable_subfinder": true,
	"enable_nmap": true,
	"search_web": true,
	"search_cve": true,
	"enable_reporting": true,

	"report_emails": ["報告先のEメールアドレス@example.com"],
	"report_limit": 2,
	"report_since_": "1970-01-01T00:00:00",
	"report_since": "2019-12-05T19:05:00",
	"report_min_cvss3": 7,
	"report_csv_encoding": "utf-8",
	"report_enable_gemini": true,
	"report_api_key": "Gemini ProのAPIキー",
	"report_enable_bcc": false,
	"report_from": "Fromとして使うEメールアドレス@example.com",

	"web_query": "",
	"web_region": "jp-jp",
	"web_max_results": 25,
	"web_backend": "html"
}
```
</details>

リクエスト例:
```bash
# 上記の設定例をconfig.jsonとして保存したあとに実行
curl -sSL "http://<バックエンドサーバーのホスト>/session/create" -X POST -H "Content-Type: application/json" -d @config.json | jq .
```

#### ASMの実行
`/asm/execute`宛に`POST`リクエストを発行することで実行できます。

例:
```bash
curl -sSLG -d session_id="<セッションID>" "http://<ホスト>/asm/execute" -X POST | jq .
```

#### 進捗状況の確認
`/progress/show`宛に`GET`リクエストを発行することで確認できます。
Nmap, CVE検索といった各タスクの進捗状況は`task_progresses`で、全体の進捗状況は`overall_progress`で確認できます。
進捗状況の値は`0.0`以上`1.0`以下の実数で、数値が高いほどその分処理が終了していることを示します。例えば`0.0`の場合0%、`0.5`の場合50%、`1.0`の場合100%処理が完了しています。

例:
```bash
curl -sSLG -d session_id="<セッションID>" "http://<ホスト>/progress/show" -X GET | jq .
```

### ファイルの説明
#### `__main__.py`
ダミーファイルです。

#### `fastapi_main.py`
メインの実行ファイルです。

#### `log.py`
ロギング関連の関数がまとまっています。

#### `context.py`
グローバル変数の代替です。

#### `routers/`
APIエンドポイント集です。

#### `schemes/`
APIエンドポイントで使われるパラメーターや戻り値の型集です。

#### `asm/`
ASMの処理がまとまっています。
subfinder, Nmap, CIRCL CVE Search, DuckDuckGo, Geminiなどの処理はここにまとまっています。

#### `asm/asm.py`
与えられた設定に応じて各サービスやツールなどを呼び出したりします。

#### `asm/proc_subfinder.py`
subfinderを用いてサブドメインを探す機能を担っています。
サブドメインが見つかった場合、見つかったサブドメインも検査対象に加えます。

#### `asm/proc_nmap.py`
Nmapを用いてサービス列挙を行う機能を担っています。

#### `asm/proc_cve.py`
Nmapから取得したCPE文字列を用いてCVE情報を取得します。
そのためNmapを実行しないよう設定した場合はこのファイルも実行されません。

#### `asm/proc_ddg.py`
DuckDuckGoで検索する機能を担っています。

#### `asm/proc_report.py`
CVE情報をGeminiに分析させたり、
Eメールを使用してCVE情報を報告する機能を担っています。

#### `requirements.txt`
依存関係についてのファイルです。
pipで利用することができます。
```bash
pip3 install -r requirements.txt
```

#### `README.md`
あなたが今読んでいる、このファイルです。

# ASM ツール

サブドメイン探索、Web 検索、サービス列挙、CVE 情報の取得、E メール報告などの機能を持つ ASM ツールです。

## 免責事項 (Disclaimer)

本ツールは教育および研究目的で提供されています。本ツールの使用による誤用、違法行為、または損害について、開発者は一切の責任を負いません。本ツールは責任を持って使用し、ネットワークやシステムをスキャンまたはテストする際には、必ず事前に適切な許可を取得してください。不正な使用は法律や規制に違反する可能性があります。

## 法的な利用範囲について (Legal Usage Notice)

本ツールを許可なくシステムやネットワークに対して使用することは厳しく禁止されています。無許可のスキャン、プロービング、テストは違法であり、法的処罰の対象となります。

### 利用規約

本ツールを使用する際、以下に同意するものとします：

- 自身が所有するネットワーク、または明示的な許可を得たネットワークにのみ使用すること。
- 不正な活動（例：無許可のデータ収集、サービス妨害攻撃、セキュリティ対策の回避）を行わないこと。
- 関連するすべてのローカル、国内、国際法を遵守すること。

## 技術的な注意事項 (Technical Notice)

- 高負荷なスキャン設定により、セキュリティ対策が作動する可能性やネットワーク性能への影響に注意してください。
- ネットワーク侵入検知システム（IDS）は、本ツールの使用を攻撃として誤検知する場合があります。
- DuckDuckGo など外部サービスのレートリミットを尊重してください。

## バックエンド

### 簡単な説明

とりあえず実行したい、そういう場合には以下のように実行してみてください。

#### Docker を使用する場合

1. start.sh or start.bat(windows)を実行(バックエンド、フロントエンドの起動)
2. localhost にアクセスし設定を行ったあと実行してください

#### Docker を使用しない場合

1. バックエンドの API サーバーの起動
2. 起動した API サーバーの`/session/create`で新規セッションの作成
3. `/asm/execute`で ASM 処理の実行
4. `/progress/show`で進捗状況の確認
5. サーバーのファイルシステムの`work/<セッションID>`配下にある結果ファイルの確認

E メール報告機能では、CVSS3 スコアの高い方から優先的にレポートするようになっています。
CVSS, CVSS3 スコアが不明なものは`-1.0`として扱われます。

#### API サーバーの実行方法

`backend/app/fastapi_main.py`を Uvicorn で実行してください。

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
リクエストボディーは JSON 形式で、設定が格納されます。
セッションの作成に成功するとセッション情報の JSON が返されます。この JSON にある`session_id`が後に使うセッション ID となりますのでご確認ください。

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

#### ASM の実行

`/asm/execute`宛に`POST`リクエストを発行することで実行できます。

例:

```bash
curl -sSL "http://<ホスト>/asm/execute" -X POST -H "Content-Type: application/json" -d "{\"session_id\": \"<セッションID>\"}" | jq .
```

#### 進捗状況の確認

`/progress/show`宛に`GET`リクエストを発行することで確認できます。
Nmap, CVE 検索といった各タスクの進捗状況は`task_progresses`で、全体の進捗状況は`overall_progress`で確認できます。
進捗状況の値は`0.0`以上`1.0`以下の実数で、数値が高いほどその分処理が終了していることを示します。
例えば`0.0`の場合 0%、`0.5`の場合 50%、`1.0`の場合 100%処理が完了しています。

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

API エンドポイント集です。

#### `schemes/`

API エンドポイントで使われるパラメーターや戻り値の型集です。

#### `asm/`

ASM の処理がまとまっています。
subfinder, Nmap, CIRCL CVE Search, DuckDuckGo, Gemini などの処理はここにまとまっています。

#### `asm/asm.py`

与えられた設定に応じて各サービスやツールなどを呼び出したりします。

#### `asm/proc_subfinder.py`

subfinder を用いてサブドメインを探す機能を担っています。
サブドメインが見つかった場合、見つかったサブドメインも検査対象に加えます。

#### `asm/proc_nmap.py`

Nmap を用いてサービス列挙を行う機能を担っています。

#### `asm/proc_cve.py`

Nmap から取得した CPE 文字列を用いて CVE 情報を取得します。
そのため Nmap を実行しないよう設定した場合はこのファイルも実行されません。

#### `asm/proc_ddg.py`

DuckDuckGo で検索する機能を担っています。

#### `asm/proc_report.py`

CVE 情報を Gemini に分析させたり、
E メールを使用して CVE 情報を報告する機能を担っています。

#### `requirements.txt`

依存関係についてのファイルです。
pip で利用することができます。

```bash
pip3 install -r requirements.txt
```

#### `README.md`

あなたが今読んでいる、このファイルです。

## サードパーティーライセンス

当 ASM ツールでは以下のプログラム、ライブラリーが使用されています(順不同)

- [duckduckgo_search](https://pypi.org/project/duckduckgo-search/) | MIT

  [LICENSE](https://github.com/deedy5/duckduckgo_search/blob/ee83d18c717d22f569f4fdc67b5e8bdfbbc7da3f/LICENSE.md)

  ```markdown
  MIT License

  Copyright (c) 2022 deedy5

  Permission is hereby granted, free of charge, to any person obtaining a copy
  of this software and associated documentation files (the "Software"), to deal
  in the Software without restriction, including without limitation the rights
  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
  copies of the Software, and to permit persons to whom the Software is
  furnished to do so, subject to the following conditions:

  The above copyright notice and this permission notice shall be included in all
  copies or substantial portions of the Software.

  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
  SOFTWARE.
  ```

- [requests](https://pypi.org/project/requests/) | Apache-2.0

  [NOTICE](https://github.com/psf/requests/blob/23540c93cac97c763fe59e843a08fa2825aa80fd/NOTICE)

  ```plain
  Requests
  Copyright 2019 Kenneth Reitz
  ```

  [LICENSE](https://github.com/psf/requests/blob/23540c93cac97c763fe59e843a08fa2825aa80fd/LICENSE)

  ```plain

                                   Apache License
                             Version 2.0, January 2004
                          http://www.apache.org/licenses/

     TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION

     1. Definitions.

        "License" shall mean the terms and conditions for use, reproduction,
        and distribution as defined by Sections 1 through 9 of this document.

        "Licensor" shall mean the copyright owner or entity authorized by
        the copyright owner that is granting the License.

        "Legal Entity" shall mean the union of the acting entity and all
        other entities that control, are controlled by, or are under common
        control with that entity. For the purposes of this definition,
        "control" means (i) the power, direct or indirect, to cause the
        direction or management of such entity, whether by contract or
        otherwise, or (ii) ownership of fifty percent (50%) or more of the
        outstanding shares, or (iii) beneficial ownership of such entity.

        "You" (or "Your") shall mean an individual or Legal Entity
        exercising permissions granted by this License.

        "Source" form shall mean the preferred form for making modifications,
        including but not limited to software source code, documentation
        source, and configuration files.

        "Object" form shall mean any form resulting from mechanical
        transformation or translation of a Source form, including but
        not limited to compiled object code, generated documentation,
        and conversions to other media types.

        "Work" shall mean the work of authorship, whether in Source or
        Object form, made available under the License, as indicated by a
        copyright notice that is included in or attached to the work
        (an example is provided in the Appendix below).

        "Derivative Works" shall mean any work, whether in Source or Object
        form, that is based on (or derived from) the Work and for which the
        editorial revisions, annotations, elaborations, or other modifications
        represent, as a whole, an original work of authorship. For the purposes
        of this License, Derivative Works shall not include works that remain
        separable from, or merely link (or bind by name) to the interfaces of,
        the Work and Derivative Works thereof.

        "Contribution" shall mean any work of authorship, including
        the original version of the Work and any modifications or additions
        to that Work or Derivative Works thereof, that is intentionally
        submitted to Licensor for inclusion in the Work by the copyright owner
        or by an individual or Legal Entity authorized to submit on behalf of
        the copyright owner. For the purposes of this definition, "submitted"
        means any form of electronic, verbal, or written communication sent
        to the Licensor or its representatives, including but not limited to
        communication on electronic mailing lists, source code control systems,
        and issue tracking systems that are managed by, or on behalf of, the
        Licensor for the purpose of discussing and improving the Work, but
        excluding communication that is conspicuously marked or otherwise
        designated in writing by the copyright owner as "Not a Contribution."

        "Contributor" shall mean Licensor and any individual or Legal Entity
        on behalf of whom a Contribution has been received by Licensor and
        subsequently incorporated within the Work.

     2. Grant of Copyright License. Subject to the terms and conditions of
        this License, each Contributor hereby grants to You a perpetual,
        worldwide, non-exclusive, no-charge, royalty-free, irrevocable
        copyright license to reproduce, prepare Derivative Works of,
        publicly display, publicly perform, sublicense, and distribute the
        Work and such Derivative Works in Source or Object form.

     3. Grant of Patent License. Subject to the terms and conditions of
        this License, each Contributor hereby grants to You a perpetual,
        worldwide, non-exclusive, no-charge, royalty-free, irrevocable
        (except as stated in this section) patent license to make, have made,
        use, offer to sell, sell, import, and otherwise transfer the Work,
        where such license applies only to those patent claims licensable
        by such Contributor that are necessarily infringed by their
        Contribution(s) alone or by combination of their Contribution(s)
        with the Work to which such Contribution(s) was submitted. If You
        institute patent litigation against any entity (including a
        cross-claim or counterclaim in a lawsuit) alleging that the Work
        or a Contribution incorporated within the Work constitutes direct
        or contributory patent infringement, then any patent licenses
        granted to You under this License for that Work shall terminate
        as of the date such litigation is filed.

     4. Redistribution. You may reproduce and distribute copies of the
        Work or Derivative Works thereof in any medium, with or without
        modifications, and in Source or Object form, provided that You
        meet the following conditions:

        (a) You must give any other recipients of the Work or
            Derivative Works a copy of this License; and

        (b) You must cause any modified files to carry prominent notices
            stating that You changed the files; and

        (c) You must retain, in the Source form of any Derivative Works
            that You distribute, all copyright, patent, trademark, and
            attribution notices from the Source form of the Work,
            excluding those notices that do not pertain to any part of
            the Derivative Works; and

        (d) If the Work includes a "NOTICE" text file as part of its
            distribution, then any Derivative Works that You distribute must
            include a readable copy of the attribution notices contained
            within such NOTICE file, excluding those notices that do not
            pertain to any part of the Derivative Works, in at least one
            of the following places: within a NOTICE text file distributed
            as part of the Derivative Works; within the Source form or
            documentation, if provided along with the Derivative Works; or,
            within a display generated by the Derivative Works, if and
            wherever such third-party notices normally appear. The contents
            of the NOTICE file are for informational purposes only and
            do not modify the License. You may add Your own attribution
            notices within Derivative Works that You distribute, alongside
            or as an addendum to the NOTICE text from the Work, provided
            that such additional attribution notices cannot be construed
            as modifying the License.

        You may add Your own copyright statement to Your modifications and
        may provide additional or different license terms and conditions
        for use, reproduction, or distribution of Your modifications, or
        for any such Derivative Works as a whole, provided Your use,
        reproduction, and distribution of the Work otherwise complies with
        the conditions stated in this License.

     5. Submission of Contributions. Unless You explicitly state otherwise,
        any Contribution intentionally submitted for inclusion in the Work
        by You to the Licensor shall be under the terms and conditions of
        this License, without any additional terms or conditions.
        Notwithstanding the above, nothing herein shall supersede or modify
        the terms of any separate license agreement you may have executed
        with Licensor regarding such Contributions.

     6. Trademarks. This License does not grant permission to use the trade
        names, trademarks, service marks, or product names of the Licensor,
        except as required for reasonable and customary use in describing the
        origin of the Work and reproducing the content of the NOTICE file.

     7. Disclaimer of Warranty. Unless required by applicable law or
        agreed to in writing, Licensor provides the Work (and each
        Contributor provides its Contributions) on an "AS IS" BASIS,
        WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
        implied, including, without limitation, any warranties or conditions
        of TITLE, NON-INFRINGEMENT, MERCHANTABILITY, or FITNESS FOR A
        PARTICULAR PURPOSE. You are solely responsible for determining the
        appropriateness of using or redistributing the Work and assume any
        risks associated with Your exercise of permissions under this License.

     8. Limitation of Liability. In no event and under no legal theory,
        whether in tort (including negligence), contract, or otherwise,
        unless required by applicable law (such as deliberate and grossly
        negligent acts) or agreed to in writing, shall any Contributor be
        liable to You for damages, including any direct, indirect, special,
        incidental, or consequential damages of any character arising as a
        result of this License or out of the use or inability to use the
        Work (including but not limited to damages for loss of goodwill,
        work stoppage, computer failure or malfunction, or any and all
        other commercial damages or losses), even if such Contributor
        has been advised of the possibility of such damages.

     9. Accepting Warranty or Additional Liability. While redistributing
        the Work or Derivative Works thereof, You may choose to offer,
        and charge a fee for, acceptance of support, warranty, indemnity,
        or other liability obligations and/or rights consistent with this
        License. However, in accepting such obligations, You may act only
        on Your own behalf and on Your sole responsibility, not on behalf
        of any other Contributor, and only if You agree to indemnify,
        defend, and hold each Contributor harmless for any liability
        incurred by, or claims asserted against, such Contributor by reason
        of your accepting any such warranty or additional liability.
  ```

- [fastapi](https://pypi.org/project/fastapi/) | MIT

  [LICENSE](https://github.com/fastapi/fastapi/blob/f9514ac4b263be971c50f7e0f719b7a6d361e192/LICENSE)

  ```plain
  The MIT License (MIT)

  Copyright (c) 2018 Sebastián Ramírez

  Permission is hereby granted, free of charge, to any person obtaining a copy
  of this software and associated documentation files (the "Software"), to deal
  in the Software without restriction, including without limitation the rights
  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
  copies of the Software, and to permit persons to whom the Software is
  furnished to do so, subject to the following conditions:

  The above copyright notice and this permission notice shall be included in
  all copies or substantial portions of the Software.

  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
  THE SOFTWARE.
  ```

- [uvicorn](https://pypi.org/project/uvicorn/) | BSD-3-Clause

  [LICENSE](https://github.com/encode/uvicorn/blob/bfa754e21e2cc1d5b0d7cabf24933a6c3afc315e/LICENSE.md)

  ```markdown
  Copyright © 2017-present, [Encode OSS Ltd](https://www.encode.io/).
  All rights reserved.

  Redistribution and use in source and binary forms, with or without
  modification, are permitted provided that the following conditions are met:

  - Redistributions of source code must retain the above copyright notice, this
    list of conditions and the following disclaimer.

  - Redistributions in binary form must reproduce the above copyright notice,
    this list of conditions and the following disclaimer in the documentation
    and/or other materials provided with the distribution.

  - Neither the name of the copyright holder nor the names of its
    contributors may be used to endorse or promote products derived from
    this software without specific prior written permission.

  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
  AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
  DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
  FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
  DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
  SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
  CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
  OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
  OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
  ```

- [gunicorn](https://pypi.org/project/gunicorn/) | MIT

  [LICENSE](https://github.com/benoitc/gunicorn/blob/bacbf8aa5152b94e44aa5d2a94aeaf0318a85248/LICENSE)

  ```plain
  2009-2024 (c) Benoît Chesneau <benoitc@gunicorn.org>
  2009-2015 (c) Paul J. Davis <paul.joseph.davis@gmail.com>

  Permission is hereby granted, free of charge, to any person
  obtaining a copy of this software and associated documentation
  files (the "Software"), to deal in the Software without
  restriction, including without limitation the rights to use,
  copy, modify, merge, publish, distribute, sublicense, and/or sell
  copies of the Software, and to permit persons to whom the
  Software is furnished to do so, subject to the following
  conditions:

  The above copyright notice and this permission notice shall be
  included in all copies or substantial portions of the Software.

  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
  OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
  NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
  HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
  WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
  OTHER DEALINGS IN THE SOFTWARE.
  ```

- [pydantic](https://pypi.org/project/pydantic/) | MIT

  [LICENSE](https://github.com/pydantic/pydantic/blob/32f405bcf6171602ffe754f1fca1681c5ddee96e/LICENSE)

  ```plain
  The MIT License (MIT)

  Copyright (c) 2017 to present Pydantic Services Inc. and individual contributors.

  Permission is hereby granted, free of charge, to any person obtaining a copy
  of this software and associated documentation files (the "Software"), to deal
  in the Software without restriction, including without limitation the rights
  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
  copies of the Software, and to permit persons to whom the Software is
  furnished to do so, subject to the following conditions:

  The above copyright notice and this permission notice shall be included in all
  copies or substantial portions of the Software.

  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
  SOFTWARE.
  ```

- [psycopg2](https://pypi.org/project/psycopg2/) | LGPL-3.0-or-later

  [LICENSE](https://github.com/psycopg/psycopg2/blob/e83754a4146d01a9bbf0b8cbf0dfd085ce9394f7/LICENSE)

  ```plain
  psycopg2 and the LGPL
  ---------------------

  psycopg2 is free software: you can redistribute it and/or modify it
  under the terms of the GNU Lesser General Public License as published
  by the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.

  psycopg2 is distributed in the hope that it will be useful, but WITHOUT
  ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
  FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public
  License for more details.

  In addition, as a special exception, the copyright holders give
  permission to link this program with the OpenSSL library (or with
  modified versions of OpenSSL that use the same license as OpenSSL),
  and distribute linked combinations including the two.

  You must obey the GNU Lesser General Public License in all respects for
  all of the code used other than OpenSSL. If you modify file(s) with this
  exception, you may extend this exception to your version of the file(s),
  but you are not obligated to do so. If you do not wish to do so, delete
  this exception statement from your version. If you delete this exception
  statement from all source files in the program, then also delete it here.

  You should have received a copy of the GNU Lesser General Public License
  along with psycopg2 (see the doc/ directory.)
  If not, see <https://www.gnu.org/licenses/>.


  Alternative licenses
  --------------------

  The following BSD-like license applies (at your option) to the files following
  the pattern ``psycopg/adapter*.{h,c}`` and ``psycopg/microprotocol*.{h,c}``:

   Permission is granted to anyone to use this software for any purpose,
   including commercial applications, and to alter it and redistribute it
   freely, subject to the following restrictions:

   1. The origin of this software must not be misrepresented; you must not
      claim that you wrote the original software. If you use this
      software in a product, an acknowledgment in the product documentation
      would be appreciated but is not required.

   2. Altered source versions must be plainly marked as such, and must not
      be misrepresented as being the original software.

   3. This notice may not be removed or altered from any source distribution.
  ```

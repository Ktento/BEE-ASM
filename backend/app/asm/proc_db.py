import psycopg2
from psycopg2 import sql
from context import Context
from log import Level
from context import Context

#dbに接続する関数
def connect_to_db(context: Context):
    try:
        connection = psycopg2.connect(
            host=context.session.server_config.host,
            port=context.session.server_config.port,
            database=context.session.server_config.database,
            user=context.session.server_config.user,
            password=context.session.server_config.password
        )
        return connection
    except Exception as e:
        context.logger.Log(Level.ERROR, f"[DB] DB connection ERROR failed: {e}")
        return False

#CVE_idをもとにCVEテーブルからaiの説明を検索する関数
def select_cve_ai(context:Context,connection, cve_id):
    try:
        # カーソルを作成してクエリを実行
        cursor = connection.cursor()
        
        # 準備
        query = sql.SQL('SELECT "AI_analysis" FROM "CVE" WHERE "CVE_id" = %s;')
        cursor.execute(query, (cve_id,))
        
        # 結果を取得
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            return False
    except Exception as e:
        context.logger.Log(Level.ERROR, f"[DB] DB connection ERROR  for CVE: {cve_id}. ERROR: {e}")
        return False
    finally:
        cursor.close()  # クエリの後にカーソルを閉じる

#insertする関数(connection:ないと実行できない(connectしたかのチェック)、table_name:テーブルの名前、columns:1次元配列で列名入力、values:2次元配列でフィールドを入力)
def insert_sql(context:Context,connection, table_name, columns, values):
    try:
        cursor = connection.cursor()
        
        # SQL文の生成
        for value in values:
            # 列名にダブルクォーテーションを追加
            escaped_columns = ['"{}"'.format(col) for col in columns]
            columns_part = ", ".join(escaped_columns)
            
            # 値を整形（文字列はエスケープ）
            escaped_values = [
                "'{}'".format(str(v).replace("'", "''")) if isinstance(v, str) else str(v)
                for v in value
            ]
            values_part = ", ".join(escaped_values)
            
            # SQL文の生成
            sql_query = f'INSERT INTO "{table_name}" ({columns_part}) VALUES ({values_part});'
            
            # SQLを実行
            cursor.execute(sql_query)
        
        # 変更をデータベースにコミット
        connection.commit()
        
    except Exception as e:
        connection.rollback()  # エラー時にロールバック
        context.logger.Log(Level.ERROR, f"[DB] DB insert ERROR  for SQL: {sql_query}. ERROR: {e}")
    finally:
        cursor.close()  # カーソルを閉じる



#dbの接続を閉じる関数
def close_connection(context:Context,connection):
    try:
        if connection:
            connection.close()
    except Exception as e:
        context.logger.Log(Level.ERROR, f"[DB] DB close ERROR: {e}")

# CVEデータの準備 (2次元配列)
# cve_data = [
#     ("CVE-2021-26472", "In VembuBDR before 4.2.0.1 and VembuOffsiteDR before 4.2.0.1 installed on Windows, the http API located at /consumerweb/secure/download.php. Using this command argument an unauthenticated attacker can execute arbitrary OS commands with SYSTEM privileges.", "VembuBDRおよびVembuOffsiteDRの古いバージョンには、/consumerweb/secure/download.phpのhttp APIに認証バイパス脆弱性があります。この脆弱性を悪用すると、攻撃者は認証なしでシステムにアクセスし、SYSTEM権限で任意のOSコマンドを実行できます。", "cpe:/o:microsoft:windows"),
#     ("CVE-2019-16463", "Adobe Acrobat and Reader versions , 2019.021.20056 and earlier, 2017.011.30152 and earlier, 2017.011.30155 and earlier version, 2017.011.30152 and earlier, and 2015.006.30505 and earlier have an untrusted pointer dereference vulnerability. Successful exploitation could lead to arbitrary code execution.", "Adobe Acrobat および Reader のバージョンには、信頼できないポインターの逆参照の脆弱性があります。この脆弱性を悪用すると、攻撃者は任意のコードを実行する可能性があります。", "cpe:/o:microsoft:windows"),
#     ("CVE-2019-16462", "Adobe Acrobat and Reader versions , 2019.021.20056 and earlier, 2017.011.30152 and earlier, 2017.011.30155 and earlier version, 2017.011.30152 and earlier, and 2015.006.30505 and earlier have a buffer error vulnerability. Successful exploitation could lead to arbitrary code execution.", "Adobe Acrobat および Reader のバージョンに存在するバッファエラー脆弱性。この脆弱性を悪用されると、任意のコードが実行される可能性があります。", "cpe:/o:microsoft:windows"),
#     ("CVE-2019-16453", "Adobe Acrobat and Reader versions , 2019.021.20056 and earlier, 2017.011.30152 and earlier, 2017.011.30155 and earlier version, 2017.011.30152 and earlier, and 2015.006.30505 and earlier have a security bypass vulnerability. Successful exploitation could lead to arbitrary code execution.", "Adobe AcrobatおよびReaderバージョンに存在するセキュリティバイパス脆弱性。悪用されると任意のコードが実行される可能性がある。", "cpe:/o:microsoft:windows")
# ]

# テーブルに挿入するための列名
# columns = ["CVE_id", "CVE_description", "AI_analysis", "CPE"]


# connection = connect_to_db(host, port, database, user, password)
# if connection:
#     # insert_sql(connection, "CVE", columns, cve_data)  # CVEデータを挿入
#     print(select_cve_ai(connection, "CVE-2021-26622"))  # 例としてCVE IDを指定
#     close_connection(connection)


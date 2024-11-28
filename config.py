#!/usr/bin/env python3
from log import Level
from datetime import datetime, timedelta

##### 全体 #####

# 検査する対象のホスト名
#TargetHosts = ["example.com", "example.net"]
TargetHosts = ["133.125.39.70"]

# subfinderとNmapの検査から除外するホスト名やネットワーク範囲。なければ空[]に
#ExcludeHosts = ["127.0.0.0/8", "example.com"]
ExcludeHosts = []

# 標準出力の色付けを有効にするか
ColorOutput = True

# 出力するログのレベル
LogLevel = Level.ALL

##### subfinder #####

# subfinderを使用するか
EnableSubfinder = True

##### レポート機能 #####

# レポートするか
EnableReporting = True

# レポート送信先のEメールアドレス
# ReportEnableBCCの設定に応じて、CCもしくはBCCで送信される
# 空にするとエラーになるため何らかのメールアドレスを入力してもらいたい
#ReportEmails = ["admin@example.com"]
ReportEmails = ["san-j22025@sist.ac.jp"]

# 何個までCVE情報をレポートするか
# 多く指定すると処理に時間が掛かるようになる
# なおCVSS3スコアの高い方から優先的にレポートするようになっている
ReportLimit = 2

# あるプラットフォームのバージョンが不明な場合、
# それの内いつ以降公開されたCVEをレポートするか
# 過去約5年分:
ReportSince = datetime.now() - timedelta(days=365 * 5)

# レポートする最小のCVSS3スコア(しきい値)
# この値未満のCVEはレポートしない
# なおCVSS3スコアが不明なものは-1.0として扱われる
# そのためすべてレポートする場合は-1.0以下に設定されたい
ReportMinCVSS3 = 7.0

# レポートに使うGemini Pro APIのキー
ReportAPIKey = "AIzaSyABkHvu23Sig59gKjRgd_t8PeJmt30uuQ4"

# CCの代わりにBCCを使うか
ReportEnableBCC = False

# レポートのFromとして使うEメールアドレス
ReportFrom = "kento333222@gmail.com"

##### Nmap #####

# Nmapを使用するか
EnableNmap = True

# Nmapに渡す追加の引数。なければ空[]に
NmapExtraArgs = []

##### Web検索機能 #####

# Web検索機能を使用するか
SearchWeb = True

# Web検索で使うクエリー。空文字列""も可
#WebQuery = "(private OR confidential OR 社外秘)"
WebQuery = ""

# Web検索で使うリージョン。これがそのままDDGS.text()に渡される
WebRegion = "jp-jp"

# Web検索結果の最大数。これもそのままDDGS.text()に渡される
WebMaxResults = 50

# Web検索で使うバックエンド。これもそのままDDGS.text()に渡される
WebBackend = "html"

##### CVE検索機能 #####

# CVE検索機能を使用するか
SearchCVE = True

# CIRCL CVE Search APIのプロトコルとホスト名を含むベースURL
CVEAPIBase = "https://cvepremium.circl.lu/api"

##### 脆弱性診断 #####
# VAT ... Vulnerability Assessment Tool

# 脆弱性診断を使用するか
EnableVAT = True

# 脆弱性診断を本当に実行するかの確認
# 実行する場合"IAmSureToRunTheVAT"を設定
RepeatAfterMeIAmSureToRunTheVAT = "IAmSureToRunTheVAT"

# VATの実行可能ファイルへのパス
VATPath = "./vat"

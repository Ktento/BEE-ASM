# フロントエンド用のNode.jsイメージ
FROM oven/bun AS build

# 作業ディレクトリを設定
WORKDIR /app

# package.jsonとpackage-lock.jsonをコピーして依存関係をインストール
COPY package.json bun.lockb ./
RUN bun install

# ソースコードをコピー
COPY . .

# フロントエンドをビルド
RUN bun run build

# 軽量なnginxイメージを使用して静的ファイルを配信
FROM nginx:alpine

# ビルドステージからdistをコピー
COPY --from=build /app/dist /usr/share/nginx/html


# ポート80を公開
EXPOSE 80

# Nginxを起動
CMD ["nginx", "-g", "daemon off;"]

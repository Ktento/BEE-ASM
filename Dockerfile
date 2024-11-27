# ベースイメージとして軽量なPythonイメージを使用
FROM python:3.10-slim

# 作業ディレクトリを設定
WORKDIR /app

# システムツールをインストール
RUN apt-get update && apt-get install -y \
    nmap \
    wget \ 
    unzip \
    git \
    golang \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Go環境の設定
ENV GOPATH=/go
ENV PATH=$GOPATH/bin:/usr/local/go/bin:$PATH

# 最新版のsubfinderのインストール
RUN wget https://github.com/projectdiscovery/subfinder/releases/download/v2.6.7/subfinder_2.6.7_linux_amd64.zip && \
    unzip subfinder_2.6.7_linux_amd64.zip && \
    mv subfinder /usr/local/bin/ && \
    rm subfinder_2.6.7_linux_amd64.zip

# 必要なPythonモジュールをインストールする準備
COPY requirements.txt .

# Pythonの依存関係をインストール
RUN pip install --no-cache-dir -r requirements.txt

# プロジェクトファイルをコンテナにコピー
COPY . .

# 必要に応じてポートを公開（デフォルト設定）
EXPOSE 8000

# コンテナ起動時のデフォルトコマンド
CMD ["python", "__main__.py"]docker build -t my-asm-tool .


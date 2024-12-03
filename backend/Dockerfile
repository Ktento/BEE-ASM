# ベースイメージとして軽量なPythonイメージを使用
FROM python:3.10-slim

# 作業ディレクトリを設定
WORKDIR /app

# 必要なパッケージをインストール
RUN apt-get update && apt-get install -y \
    gcc \
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

# Pythonの依存関係をインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# FastAPIアプリケーションをコピー
COPY app /app

# Uvicornを使用してFastAPIアプリケーションを起動
CMD ["uvicorn", "fastapi_main:app", "--host", "0.0.0.0", "--port", "8000"]


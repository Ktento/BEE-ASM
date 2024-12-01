# ベースイメージとして軽量なPythonイメージを使用
FROM python:3.10-slim

# 作業ディレクトリを設定
WORKDIR /app

# 必要なパッケージをインストール
RUN apt-get update && apt-get install -y \
    gcc \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Pythonの依存関係をインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# FastAPIアプリケーションをコピー
COPY app /app

# Uvicornを使用してFastAPIアプリケーションを起動
CMD ["uvicorn", "fastapi_main:app", "--host", "0.0.0.0", "--port", "8000"]


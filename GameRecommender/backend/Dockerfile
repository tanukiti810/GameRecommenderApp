FROM python:3.10-slim

# 作業ディレクトリ
WORKDIR /app

# 依存関係を先にコピー
COPY requirements.txt .

# 必要なライブラリをインストール
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーション本体をコピー
COPY app ./app

# 開発用：ホットリロード有効
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]


# ---------------------
# FastAPI Backend (PROD)
# ---------------------
# FROM python:3.10-slim

# WORKDIR /app

# # pipだけでなく OS パッケージも最小限インストール
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     build-essential && \
#     rm -rf /var/lib/apt/lists/*

# COPY requirements.txt .

# RUN pip install --no-cache-dir -r requirements.txt

# COPY app ./app

# # reload なし（本番モード）
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# ベースイメージ
FROM node:18

# 作業ディレクトリを設定
WORKDIR /app

# 必要なファイルをコピー
COPY package.json package.json
COPY tsconfig.json tsconfig.json
COPY src src
COPY public public

# 依存関係をインストール
RUN npm install

# Reactアプリケーションを起動
CMD ["npm", "start"]


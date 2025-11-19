FROM node:18

# コンテナ内作業ディレクトリ
WORKDIR /app

# 依存関係ファイルだけコピー
COPY package.json package.json
COPY package-lock.json package-lock.json

# 依存関係インストール（キャッシュが効く）
RUN npm install

# ソースコードは docker-compose の volumes でマウントするため COPY しない

# 開発サーバー起動
CMD ["npm", "start"]


# ---------------------
# Frontend PROD build
# ---------------------
# FROM node:18 AS builder

# WORKDIR /app

# COPY package.json package-lock.json ./
# RUN npm install

# COPY . .
# RUN npm run build


# # 本番用（軽量サーバー）
# FROM nginx:stable-alpine

# COPY --from=builder /app/build /usr/share/nginx/html
# EXPOSE 80

# CMD ["nginx", "-g", "daemon off;"]

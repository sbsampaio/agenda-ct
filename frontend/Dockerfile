# --- Build Stage ---
FROM node:18-alpine AS builder
WORKDIR /app

# Docker compose argument and env variable
ARG VUE_APP_API_BASE_URL
ENV VUE_APP_API_BASE_URL=${VUE_APP_API_BASE_URL}

COPY package*.json ./
COPY . .
RUN npm install

RUN npm run build

# --- Production Stage ---
FROM nginx:1.25-alpine
COPY --from=builder /app/dist/spa /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
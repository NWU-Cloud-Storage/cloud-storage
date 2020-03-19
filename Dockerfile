# Stage 0: build frontend
FROM node:13.10-alpine3.10

# ENV BUILD_ENV=production

COPY ./frontend /app
WORKDIR /app
RUN npm install --registry=https://registry.npm.taobao.org && \
    npm run build

# Stage 1: build backend and configure nginx
FROM python:3.8-alpine3.10

COPY --from=0 /app/dist /app/dist
COPY . /app
WORKDIR /app/backend

RUN sed -i "s/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g" /etc/apk/repositories && \   
    apk --update add --no-cache nginx supervisor && \
    pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

EXPOSE 80
ENTRYPOINT /app/deploy/entrypoint.sh
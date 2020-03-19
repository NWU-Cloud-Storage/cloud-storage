FROM alpine:3.11

COPY . /root/
WORKDIR /root/backend

RUN sed -i "s/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g" /etc/apk/repositories && \   
    apk --update add --no-cache nginx python3 nodejs py3-pip && \
    pip3 install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

WORKDIR /root/frontend
RUN npm install --registry=https://registry.npm.taobao.org && \
    npm run build

EXPOSE 8000
ENTRYPOINT /root/deploy/entrypoint.sh
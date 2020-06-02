# Frontend

## 开发环境

- @vue/cli 4.0.5

其余依赖见`package.json`。

## 目录结构

src 为源代码：入口点 main.js

主界面 App.vue

## Data structure

进入下一级路径时，上一级的数据？

在路由中记录路径

### 如何实现进入文件夹

如果不使用路由的话，就不能实现浏览器的前进后退来进行文件夹的前进后退。

重命名在选中多个文件时不可见。

### 上传文件

拖放上传

- 拖放至任意处上传
- 拖放到一个文件夹即上传至这个文件夹

## API 的维护

在全局配置文件中定义 api_base

## 优点

- 组件化，减少冗余代码

- 数据双向绑定，实时响应用户的操作
- 界面简洁易用

## 构建

### npm 本地构建

本地构建时，使用`BUILD_ENV=production`标志生产环境构建，此时 eslint 将更加严格。

```sh
npm run build
```

### 容器化构建

容器化构建时，默认采用生产环境模式构建。
要忽略不必要的警告，请注释掉[dockerfile](../../frontend/dockerfile)第十行。

```sh
cd frontend
# powershell
./build
# sh
sh build.ps1
```

### 运行

```sh
docker run -d -p 80:80 cloud-storage-front
```

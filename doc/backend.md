# 后端版本、配置、依赖项等

## 依赖
见`requirements.txt`

## 初始化

- makemigrations
- migrate
- createsuperuser

## 权限管理

两种权限模型:

### 按角色分

- 读
- 读写
- 所有者

### 按权限细分

- 查看文件
- 创建文件
- 修改文件
- 删除文件
- 添加成员
- 删除成员
- 修改他人权限

Keep It Simple and Stupid? (误)

那就采用第一种吧
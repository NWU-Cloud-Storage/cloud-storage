# 后端版本、配置、依赖项等

## 依赖
见`requirements.txt`

后端初始化

```bash
cd backend
python3 manage.py makemigrations user
python3 manage.py makemigrations group
python3 manage.py makemigrations storage
python3 manage.py makemigrations share
python3 manage.py migrate
python3 manage.py createsuperuser # 创建超级管理员（自己）
```

启动服务

```cmd
python3 manage.py runserver
```

在浏览器输入http://127.0.0.1:8000/admin/进入管理员页面

## 清华大学镜像

```cmd
pip install xxx -i https://pypi.tuna.tsinghua.edu.cn/simple
```

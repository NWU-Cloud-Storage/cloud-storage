# 前后端接口设计说明书

## User 用户

### 获取某用户资料

* Url: `/api/user/2017110048/`
* Method: `GET`
* Return: `json`

```json
{
    "msg": "success",
    "result": {
        "username": "2017110048",
        "nickname": "zjb",
    }
}
```

### 获取个人全部资料

* Url: `/api/user/`
* Method: `GET`
* Return: `json`

```json
{
    "msg": "success",
    "result": {
        "username": "2017110048",
        "nickname": "zjb",
        "max_size": 123123123,
        "used_size": 123123,
    }
}
```

### 修改个人资料

* Url: `/api/user/`
* Method: `PUT`
* Body: `json`

```json
{
    "nickname": "zhangjunbo"
}
```

* Return: `json`

```json
{
    "msg": "success",
    "result": {}
}
```

### **登入**

?

### **退出**

?

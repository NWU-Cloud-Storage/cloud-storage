# 前后端接口设计说明书

## User 用户

### 获取某用户资料

* Url: `/api/user/2017110048/`
* Method: `GET`
* Return: `200 OK`

```json
{
    "username": "2017110048",
    "nickname": "zjb",
}
```

### 获取个人全部资料

* Url: `/api/user/`
* Method: `GET`
* Return: `200 OK`

```json
{
    "username": "2017110048",
    "nickname": "zjb",
    "max_size": 123123123,
    "used_size": 123123,
    "date_last_opt": "2019-11-30T15:34:42.257461+08:00"
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

* Return: `200 OK`

```json
{}
```

* Errors: `400 BAD REQUEST`

### **登入**

?

### **退出**

?

# 前后端接口设计说明书

## Share 分享

### 创建分享链接

* Url: `/api/share/109[目录id]/30[天数，不填为无限]/`
* Method: `POST`
* Return: `json`

```json
{
    // "code": "401",
    "msg": "success",
    "result":{
        "url": "xbabasdasd",
        "pwd": "1234",
        "expiration": "2020-3-2 19:00:00",
    }
}
```

### 分享到群组

* Url: `/api/share_to_group/3[群组id]/109[目录id]/110[群组目录id]/`
* Method: `POST`
* Return: `json`

```json
{
    // "code": "402",
    "msg": "success",
    "result": {}
}
```

### 保存别人的分享到个人仓库

* Url: `/api/share_to_me/xbabasdasd[分享url]/233[个人仓库id，不填为根目录]/`
* Method: `PUT`
* Return: `json`

```json
{
    // "code": "403",
    "msg": "success",
    "result": {}
}
```

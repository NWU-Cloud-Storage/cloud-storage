# 前后端接口设计说明书

## Group 群组

### 获取个人全部群组

* Url: `/api/my_group/`
* Method: `GET`
* Return: `200 OK`

```json
[
    {
        "id": 3,
        "name": "重案六组",
        "member_number": 60,
        "my_permission": "master"
    },{
        "id": 12,
        "name": "日语资料分享群",
        "member_number": 122,
        "my_permission": "memeber"
    }
]
```

### 获取某群组详细信息

* Url: `/api/my_group/12/`
* Method: `GET`
* Return: `200 OK`

```json
{
    "id": 12,
    "name": "日语资料分享群",
    "member_number": 122,
    "members": [
        {
            "username": "2017110048",
            "nickname": "zjb",
            "permission": "member"
        },{
            "username": "9017123456",
            "nickname": "老司机",
            "permission": "master"
        }
    ]
}
```

### 修改某群组信息

* Url: `/api/my_group/12/`
* Method: `PUT`
* Body: `json`

```json
{
    "name": "正经学习群",
}
```

* Return: `200 OK`

```json
{}
```

### 建立一个新群组

* Url: `/api/my_group/`
* Method: `POST`
* Return: `200 OK`

```json
{
    "id": 36,
    "name": "zjb的小组"
}
```

### 解散一个群组

* Url: `/api/my_group/36/`
* Method: `DELETE`
* Return: `200 OK`

```json
{}
```

### 踢掉一个成员

* Url: `/api/membership/36[群组id]/9012123456[用户名]/`
* Method: `DELETE`
* Return: `200 OK`

```json
{}
```

### 请求加入一个群

* Url: `/api/intention/36/`
* Method: `POST`
* Return: `200 OK`

```json
{}
```

### 查看某群的请求加入列表

* Url: `/api/intention/36/`
* Method: `GET`
* Return: `200 OK`

```json
[
    {
        "username": "2017110048",
        "nickname": "zjb",
        "date_intented": "2017-12-12 08:12:12" //申请时间
    },{
        "username": "9012110048",
        "nickname": "richzjb",
        "date_intented": "2017-12-12 08:12:12"
    }
]
```

### 同意某人的加入申请

* Url: `/api/intention/36/2017110048/`
* Method: `POST`
* Return: `200 OK`

```json
{}
```

### 拒绝某人的加入申请

* Url: `api/intention/36/2017110048/`
* Method: `DELETE`
* Return: `200 OK`

```json
{}
```

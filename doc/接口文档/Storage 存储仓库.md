# 前后端接口设计说明书

## Storage 存储仓库

### 获取个人仓库根目录

* Url: `/api/my_storage/`
* Method: `GET`
* Return: `200 OK`

```json
[
    {
        "id": 71,
        "name": "日语学习资料",
        "is_file": false,
        "is_shared": false,
        "modified_date": "2019-11-30T15:34:42.257461+08:00"
    },{
        "id": 103,
        "name": "那个自由♂男人",
        "is_file": true,
        "size": 10241024,
        "extension": "avi",
        "is_shared": false,
        "modified_date": "2019-11-30T15:34:42.257461+08:00"
    }
]
```

### 获取个人仓库某文件夹内容

* Url: `/api/my_storage/71[目录id]/`
* Method: `GET`
* Return: `200 OK`

```json
[
    {
        "id": 109,
        "name": "すごい AV机器",
        "is_file": true,
        "size": 101234,
        "extension": "mp4",
        "is_shared": false,
        "modified_date": "2019-11-30T15:34:42.257461+08:00"
    },{
        "id": 110,
        "name": "やばい! おフェロ女子",
        "is_file": true,
        "size": 1021443,
        "extension": "flv",
        "is_shared": false,
        "modified_date": "2019-11-30T15:34:42.257461+08:00"
    },{
        "id": 78,
        "name": "最新写真集",
        "is_file": false,
        "is_shared": false,
        "modified_date": "2019-11-30T15:34:42.257461+08:00"
    }
]
```

### 删除个人仓库某文件(夹)

* Url: `/api/my_storage/`
* Method: `DELETE`
* Body: `json`

```json
{
    "id": //[源目录id]
    [
        12,
        13,
        14
    ]
}
```

* Return: `200 OK`

```json
{}
```

### 修改个人仓库某文件(夹)

* Url: `/api/my_storage/71/`
* Method: `PATCH`
* Body: `json`

```json
{
    "name": "青年大学习资料",
    //如果是文件要有下面的接口
    "extension": "txt",
}
```

* Return: `200 OK`

```json
{}
```

### 在个人仓库新建文件夹

* Url: `/api/my_storage/71/`
* Method: `POST`
* Return: `200 OK`

```json
{
    "id": 74,
    "name": "新建文件夹"
}
```

### 移动个人仓库文件(夹)

* Url: `/api/my_storage/move/99/`
* Method: `PUT`
* Body: `json`

```json
{
    "id": //[源目录id]
    [
        12,
        13,
        14
    ]
}
```

* Return: `200 OK`

```json
{}
```

### 获取某群组仓库根目录

* Url: `/api/group_storage/3[群组id]/`
* Method: `GET`
* Return: `200 OK`

```json
[
    {
        "id": 98,
        "name": "省下发文件",
        "is_file": false,
        "is_shared": false,
        "modified_date": "2019-11-30T15:34:42.257461+08:00"
    },{
        "id": 103,
        "name": "扫黄打飞注意事项",
        "is_file": true,
        "size": 3150,
        "extension": "doc",
        "is_shared": false,
        "modified_date": "2019-11-30T15:34:42.257461+08:00"
    }
]
```

### 获取某群组仓库某文件夹内容

* Url: `/api/group_storage/3[群组id]/98[目录id]/`
* Method: `GET`
* Return: `200 OK`

```json
[
    {
        "id": 219,
        "name": "钓鱼执法的必要性",
        "is_file": true,
        "size": 51234,
        "extension": "doc",
        "is_shared": false,
        "modified_date": "2019-11-30T15:34:42.257461+08:00"
    },{
        "id": 220,
        "name": "《人民的名义》电视连续剧",
        "is_file": false,
        "is_shared": false,
        "modified_date": "2019-11-30T15:34:42.257461+08:00"
    }
]
```

### 删除某群组仓库某文件(夹)

* Url: `/api/group_storage/98/`
* Method: `DELETE`
* Body: `json`

```json
{
    "id": //[源目录id]
    [
        12,
        13,
        14
    ]
}
```

* Return: `200 OK`

```json
{}
```

### 修改某群组仓库某文件(夹)

* Url: `/api/group_storage/3/98/`
* Method: `PATCH`
* Body: `json`

```json
{
    "name": "青年大学习资料",
    //如果是文件要有下面的接口
    "extension": "txt",
}
```

* Return: `200 OK`

```json
{}
```

### 在群组仓库新建文件夹

* Url: `/api/group_storage/3/98/`
* Method: `POST`
* Return: `200 OK`

```json
{
    "id": 100,
    "name": "新建文件夹"
}
```

### 移动群组仓库文件(夹)

* Url: `/api/group_storage/move/3/99/`
* Method: `PUT`
* Body: `json`

```json
{
    "id": //[源目录id]
    [
        12,
        13,
        14
    ]
}
```

* Return: `200 OK`

```json
{}
```

### **上传文件**

？

### **下载文件**

?

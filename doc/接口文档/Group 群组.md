# 前后端接口设计说明书

## Group 群组

### 获取个人全部群组

* Request
  * Url: `/api/my-group/`
  * Method: GET

* Response
  * Status Code: 200 OK

    ```json
    [
        {
            "id": 3,
            "name": "重案六组",
            "num_of_members": 60,
            "permission": "master"
        },{
            "id": 12,
            "name": "日语资料分享群",
            "num_of_members": 122,
            "permission": "memeber"
        }
    ]
    ```

### 获取某群组详细信息

* Request
  * Url: `/api/my-group/12/`
  * Method: GET

* Response
  * Status Code: 200 OK

    ```json
    {
        "id": 12,
        "name": "日语资料分享群",
        "num_of_members": 122,
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

* Request
  * Url: `/api/my-group/12/`
  * Method: PUT
  * Content-Type: application/json
  * Body:

    ```json
    {
        "name": "正经学习群",
    }
    ```

* Response
  
  * Status Code: 200 OK

### 建立一个新群组

* Request
  * Url: `/api/my-group/`
  
  * Method: POST
  
  * Content-Type: application/json
  
  * Body:
  
    ```json
    {
        "name": "开车群"
    }
    ```
  
    
* Response
  * Status Code: 200 OK

    ```json
    {
        "id": 36,
        "name": "zjb的小组"
    }
    ```

### 解散/退出一个群组

* Request
  * Url: `/api/my-group/36/`
  * Method: DELETE

* Response
  * Status Code: 200 OK

### 修改成员权限

* Request
  * Url: `/api/membership/36[群组id]/9012123456[用户名]/`
  * Method: PUT
  * Content-Type: application/json
  * Body:

    ```json
    {
        "premission": "manager" // "member"
    }
    ```

* Response
  
  * Status Code: 200 OK

### 踢掉一个成员

* Request
  * Url: `/api/membership/36[群组id]/9012123456[用户名]/`
  * Method: DELETE

* Response
  * Status Code: 200 OK

### 请求加入一个群

* Request
  * Url: `/api/intention/36/`
  * Method: POST

* Response
  * Status Code: 200 OK

### 查看某群的请求加入列表

* Request
  * Url: `/api/intention/36/`
  * Method: GET

* Response
  * Status Code: 200 OK

```json
[
    {
        "username": "2017110048",
        "nickname": "zjb",
        "date_intented": "2019-11-30T15:34:42.257461+08:00" //申请时间
    },{
        "username": "9012110048",
        "nickname": "richzjb",
        "date_intented": "2019-11-30T15:34:42.257461+08:00"
    }
]
```

### 同意某人的加入申请

* Request
  * Url: `/api/intention/36/2017110048/`
  * Method: POST

* Response
  * Status Code: 200 OK

### 拒绝某人的加入申请

* Request
  * Url: `api/intention/36/2017110048/`
  * Method: DELETE

* Response
  * Status Code: 200 OK

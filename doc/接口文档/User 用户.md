# 前后端接口设计说明书

## User 用户

### 获取某用户资料

* Request
  * Url: `/api/user/2017110048/`
  * Method: GET

* Response
  * Status Code: 200 OK

    ```json
    {
        "username": "2017110048",
        "nickname": "zjb",
    }
    ```

### 获取个人全部资料

* Request
  * Url: `/api/user/`
  * Method: GET

* Response
  * Status Code: 200 OK

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

* Request
  * Url: `/api/user/`
  * Method: PUT
  * Content-Type: application/json
  * Body:

    ```json
    {
        "nickname": "zhangjunbo"
    }
    ```

* Response
  * Status Code: 200 OK

### **登入**

?

### **退出**

?

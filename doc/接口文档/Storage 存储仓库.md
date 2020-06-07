# Storage 存储仓库

## 存储仓库的管理

### 获取个人的所有仓库列表

* Request

  * Url: `/api/storage/`

  * Method: GET

* Response

  * Status Code: 200OK

  * Body:

    ```json
    [
        {
        	'storage_id': 100
    	}
    ]
    ```

### 获取仓库的详细信息

* Request
  * Url: `/api/storage/12[仓库id]/`
  * Method: GET
  
* Response：

  * Body:

    ```json
    {
        "storage_id": 12,
        "name": "123",
        "root_folder_id": 80,
        "is_personal_storage": false,
        
    }
    ```
    

### 创建存储库

* Request

  * Url: `/api/storage/`

  * Method: POST

  * Body:

    ```json
    {
        "name": "测试群"
    }
    ```


* Response

  * Status Code: 200OK

  * Body:

    ```json
    [
        {
        	'storage_id': 100
    	}
    ]
    ```


### 修改某存储库信息

- Request
  - Url: `/api/storage/12/`

  - Method: PUT

  - Body:

  ```json
  {
      "name": "测试群"
  }
  ```



### 删除（退出）一个存储库

- Request
  - Url: `/api/storage/12/`
  - Method: DELETE
- Response
  - 若用户为该存储库的唯一 owner，或为个人存储库，则不可执行该操作
  
    

## 仓库成员管理

### 获取成员列表

- Request

  - Url: `/api/storage/12/member/`
  - Method: GET

- Response

  - Body:

    ```json
    [
            {
                "username": "2017110048",
                "nickname": "zjb",
                "permission": "member"
            },
            {
                "username": "9017123456",
                "nickname": "老司机",
                "permission": "master"
            }
    ]
    ```

### 添加一个成员

应该要有两种方式，通过链接进入和直接通过学号添加。

#### 通过学号添加

- Request

  - Url: `/api/storage/12/member/`

  - Method: PUT

  - Body:

    ```json
    {
        "username": "2017118273"
    }
    ```
  
- Response

  - 用户不存在

    - Status Code: 404

    - Body:

      ```json
      {
          "msg": "用户不存在."
      }
      ```

      

#### 通过邀请链接进入

* Request

  * Url: `/api/storage/join/`

  * Method: PUT

  * Body:

    ```json
    {
        "token": "kalsdjf203jfidkfldsn"
    }
    ```

* Response

  * token 无效
    * Status Code: 404 Not Found

### 查看可用权限列表

- Request

  - Url: `/api/storage/permissions/`
  - Method: GET

- Response

  - Body:

    ```json
    [
        {
            "name": "读",
            "value": "read"
        },
        {
            "name": "读写",
            "value": "read_write"
        },
        {
            "name": "所有者",
            "value": "owner"
        },
    ]
    ```

    

### 修改成员的权限

- Request

  - Url: `/api/storage/12/member/20171162172[username]/`

  - Method: PUT

  - Body:

    ```json
    {
        "permission": "owner"
    }
    ```

### 移除一个成员

- Request
  - Url: `/api/storage/12/member/20171162172[username]/`

  - Method: DELETE

## 仓库内容管理

### 获取某文件夹内容

* Request
  * Url: `/api/storage/12[仓库id]/71[目录id]/`
  * Method: GET

* Response
  * Status Code: 200 OK

  * 面包屑的顺序为从根目录向下直到自身
  
    ```json
    {
        "breadcrumbs": [
            {
                "id": 100,
                "name": "File"
            }
        ],
        "content": [
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
    }
    ```

### 删除仓库某文件(夹)

只能够删除当前目录下的文件.

* Request
  * Url: `/api/storage/12[仓库id]/71/`
  * Method: DELETE
  * Content-Type: application/json
  * Body:

    ```json
    {
        "id": //[要删除的目录id]
        [
            12,
            13,
            14
        ]
    }
    ```


* Response
  
  * Status Code: 200 OK

### 修改仓库某文件(夹)

* Request
  * Url: `/api/storage/12[仓库id]/71/`
  * Method: PUT
  * Content-Type: application/json
  * Body:

    ```json
    {
        "name": "青年大学习资料",
        //如果是文件要有下面的接口
        "extension": "txt",
    }
	  ```

* Response
  
  * Status Code: 200 OK

### 在仓库新建文件夹

* Request
  
  * Url: `/api/storage/12[仓库id]/71/`
  
* Method: POST
  
  * Content-Type: application/json
  
  * Body:
  
    ```json
    {
        "name": "新建文件夹"
    }
    ```
  
    
  
* Response
  * Status Code: 200 OK

    ```json
    {
        "id": 74,
        "name": "新建文件夹"
    }
    ```

### 移动仓库文件(夹)

* Request
  * Url: `/api/storage/12[仓库id]/80[目录id]/move/`
  * Method: PUT
  * Content-Type: application/json
  * Body:

    ```json
    {
        "source_id":
        [
            12,
            13,
            14
        ],
        "destination_storage_id": 12,
        "destination_directory_id": 10
    }
    ```
  
  
  
* Response
  
  * Status Code: 200 OK
  
  
  
### 复制仓库文件(夹)

* Request
  * Url: `/api/storage/12[仓库id]/80[目录id]/copy/`
  * Method: PUT
  * Content-Type: application/json
  * Body:

    ```json
    {
        "source_id":
        [
            12,
            13,
            14
        ],
        "destination_storage_id": 12,
        "destination_directory_id": 10
    }
    ```
  
  
  
* Response

  * Status Code: 200 OK
  
### **上传文件**

* Request

  * Url: `/api/storage/upload/[仓库id]/80[目录id]/[文件夹id]/`

  * Method: POST

  * Content-Type: multipart/form-data

  * Body:

    ```json
    file: <baniry>
    data: {}
    ```
  
* Response

  * Status Code: 200OK

### **下载文件**

AJAX下载有锅！！

* Request

  * Url: `/api/storage/download/[id]/`

  * Method: GET

* Response

  * Status Code: 200OK

目前取消了下载接口的授权验证。

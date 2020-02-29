# Storage 存储仓库

## 存储仓库

### 获取仓库内容

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

* Request
  * Url: `/api/storage/12[仓库id]/`
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
  * Url: `/api/storage/12[仓库id]/move/`
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
  * Url: `/api/storage/12[仓库id]/copy/`
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

  * Url: `/api/storage/upload/[id]/`

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

## 个人存储仓库

### 获取个人仓库内容

在存储仓库基础上新增一个接口`/api/storage/0/`(`/api/storage/my/`? 待定)

# Storage 存储仓库

## 个人仓库

### 获取个人仓库内容

* Request
  * Url: `/api/my-storage/71[目录id]/`或`/api/my-storage/`
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

### 删除个人仓库某文件(夹)

* Request
  * Url: `/api/my-storage/`
  * Method: DELETE
  * Content-Type: application/json
  * Body:

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

* Response
  
  * Status Code: 200 OK

### 修改个人仓库某文件(夹)

* Request
  * Url: `/api/my-storage/71/`
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

### 在个人仓库新建文件夹

* Request
  * Url: `/api/my-storage/71/`
  * Method: POST

* Response
  * Status Code: 200 OK

    ```json
    {
        "id": 74,
        "name": "新建文件夹"
    }
    ```

### 移动个人仓库文件(夹)

* Request
  * Url: `/api/my-storage/move/`
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
        "destination_id": 10
    }
    ```

* Response
  
  * Status Code: 200 OK
  
  
  
### 复制个人仓库文件(夹)

* Request
  * Url: `/api/my-storage/copy/`
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
        "destination_id": 10
    }
    ```

* Response

  * Status Code: 200 OK
  
  
  
### 复制个人仓库文件(夹)

* Request
  * Url: `/api/my-storage/copy/`
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
        "destination_id": 10
    }
    ```

* Response

  * Status Code: 200 OK

### **上传文件**

？

### **下载文件**

?

## 群组仓库

### **上传文件**

？

### **下载文件**

?

## 群组仓库

### 获取某群组仓库根目录

* Request
  * Url: `/api/group-storage/3[群组id]/`
  * Method: GET

* Response
  * Status Code: 200 OK

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

* Request
  * Url: `/api/group-storage/3[群组id]/98[目录id]/`
  * Method: GET

* Response
  * Status Code: 200 OK

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

* Request
  * Url: `/api/group-storage/3/`
  * Method: DELETE
  * Content-Type: application/json

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

* Response
  
  * Status Code: 200 OK

### 修改某群组仓库某文件(夹)

* Request
  * Url: `/api/group-storage/3/98/`
  * Method: PUT
  * Content-Type: application/json

    ```json
    {
        "name": "青年大学习资料",
        //如果是文件要有下面的接口
        "extension": "txt",
    }
    ```

* Response
  
  * Status Code: 200 OK

### 在群组仓库新建文件夹

* Request
  * Url: `/api/group-storage/3/98/`
  * Method: POST

* Response
  * Status Code: 200 OK

    ```json
    {
        "id": 100,
        "name": "新建文件夹"
    }
    ```

### 移动群组仓库文件(夹)

* Request
  * Url: `/api/group-storage/move/3/`
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
        "destination_id": 10
    }
    ```

* Response
  
  * Status Code: 200 OK

## 个人仓库与群组仓库

### 上传到群组

* Request
  * Url: `/api/upload-to-group/3[群组id]/110[群组目录id]/`
  * Method: POST
  * Content-Type: application/json
  * Body:

    ```json
    {
        "id": //[个人仓库源目录id]
        [
            12,
            13,
            14
        ]
    }
    ```

* Response
  * Status Code: 200 OK

### 保存到个人仓库

* Request
  * Url: `/api/save-to-my-storage/3[群组id]/322[个人目录id]/`
  * Method: POST
  * Content-Type: application/json
  * Body:

    ```json
    {
        "id": //[群组仓库源目录id]
        [
            102,
            103,
            104
        ]
    }
    ```

* Response
  * Status Code: 200 OK

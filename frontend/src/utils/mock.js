import Mock from 'mockjs'

// const Random = Mock.Random;
Mock.setup({
    timeout: 800
})
//使用mockjs模拟数据
Mock.mock('/api/my-storage/', () => {//当post或get请求到/api/data路由时Mock会拦截请求并返回上面的数据
    return {
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
                "name": "文件夹1",
                "is_file": false,
                "is_shared": false,
                "modified_date": "2019-11-30T15:34:42.257461+08:00"
            }
        ]
    }
})

Mock.mock('/api/my-storage/100/', () => {//当post或get请求到/api/data路由时Mock会拦截请求并返回上面的数据
    return {
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
                "name": "文件夹1",
                "is_file": false,
                "is_shared": false,
                "modified_date": "2019-11-30T15:34:42.257461+08:00"
            }
        ]
    }
})

Mock.mock('/api/my-storage/78/', () => {
    return {
        "breadcrumbs": [
            {
                "id": 100,
                "name": "File"
            },
            {
                "id": 78,
                "name": "文件夹1"
            }
        ],
        "content": [
            {
                "id": 119,
                "name": "すごい AV机器",
                "is_file": true,
                "size": 101234,
                "extension": "mp4",
                "is_shared": false,
                "modified_date": "2019-11-30T15:34:42.257461+08:00"
            }
        ]
    }
})

Mock.mock('/api/file/72/', () => {
    return [{
        "id": 106,
        "name": "文件3",
        "is_file": true,
        "size": 10241024,
        "extension": "avi",
        "is_shared": false,
        "modified_date": "2019-11-24"
    }]
})

Mock.mock('/api/test/', () => {
    return
})

Mock.mock('/api/my-storage/move/', () => {
    return
})
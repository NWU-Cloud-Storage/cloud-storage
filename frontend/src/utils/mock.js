import Mock from 'mockjs'

// const Random = Mock.Random;
Mock.setup({
    timeout: 800
})
//使用mockjs模拟数据
Mock.mock('/api/file/', () => {//当post或get请求到/api/data路由时Mock会拦截请求并返回上面的数据
    return [
        {
            "id": 71,
            "name": "文件夹1",
            "is_file": false,
            "is_shared": false,
            "modified_date": "2019-11-24"
        }, {
            "id": 103,
            "name": "那个自由♂男人",
            "is_file": true,
            "size": 10241024,
            "extension": "avi",
            "is_shared": false,
            "modified_date": "2019-11-24"
        }
    ]
})

Mock.mock('/api/file/71/', () => {
    return [
        {
            "id": 72,
            "name": "文件夹2",
            "is_file": false,
            "is_shared": false,
            "modified_date": "2019-11-24"
        }, {
            "id": 104,
            "name": "文件2",
            "is_file": true,
            "size": 10241024,
            "extension": "avi",
            "is_shared": false,
            "modified_date": "2019-11-24"
        }
    ]
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
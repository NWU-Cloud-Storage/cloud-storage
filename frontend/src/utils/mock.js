import Mock from 'mockjs'

// const Random = Mock.Random;
Mock.setup({
    timeout: 800
})
//使用mockjs模拟数据
Mock.mock('/api/file/', () => {//当post或get请求到/api/data路由时Mock会拦截请求并返回上面的数据
    let list = [];
    let listObject1 = {
        fileName: "文件夹1",
        modifiedDate: "2019-11-25",
        shareStatus: "私有",
        size: "",
        isDirectory: true
    };
    let listObject2 = {
        fileName: "文件1",
        modifiedDate: "2019-11-25",
        shareStatus: "私有",
        size: "1.5MB",
        isDirectory: false
    };
    list.push(listObject1);
    list.push(listObject2);
    return {
        data: list
    }
})

Mock.mock('/api/file/文件夹1/', () => {
    let list = [];
    let listObject1 = {
        fileName: "文件夹2",
        modifiedDate: "2019-11-25",
        shareStatus: "私有",
        size: "",
        isDirectory: true
    };
    let listObject2 = {
        fileName: "文件2",
        modifiedDate: "2019-11-25",
        shareStatus: "私有",
        size: "1.5MB",
        isDirectory: false
    };
    list.push(listObject1);
    list.push(listObject2);
    return {
        data: list
    }
})

Mock.mock('/api/file/文件夹1/文件夹2/', () => {
    let list = [];
    let listObject2 = {
        fileName: "文件3",
        modifiedDate: "2019-11-25",
        shareStatus: "私有",
        size: "1.5MB",
        isDirectory: false
    };
    list.push(listObject2);
    return {
        data: list
    }
})
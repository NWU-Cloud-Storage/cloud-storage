import Mock from 'mockjs'

// const Random = Mock.Random;
//使用mockjs模拟数据
Mock.mock('/api/data', () => {//当post或get请求到/api/data路由时Mock会拦截请求并返回上面的数据
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
    // for(let i = 0; i < 30; i++) {
    //     let listObject = {
    //         fileName: Random.cname(),
    //         modifiedDate: Random.date(),
    //         shareStatus: Random.boolean() ? "私有" : "已共享",
    //         size: Random.float(0, 100),
    //         isDirectory: Random.boolean()
    //     }
    //     list.push(listObject);
    // }
    return {
        data: list
    }
})
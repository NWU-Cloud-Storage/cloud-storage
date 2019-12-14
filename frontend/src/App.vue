<template>
    <el-container style="height: 1000px; border: 1px solid #eee">
        <el-header height="150px">
            <Header></Header>
        </el-header>
        <el-container direction="horizontal">
            <el-aside>
                <div id="nav">
                    <el-menu>
                        <router-link to="/">
                            <el-menu-item>文件</el-menu-item>
                        </router-link>

                        <router-link to="/share/">
                            <el-menu-item>共享</el-menu-item>
                        </router-link>

                        <router-link to="/about">
                            <el-menu-item>关于</el-menu-item>
                        </router-link>
                    </el-menu>
                </div>
            </el-aside>
            <el-main>
                <div id="app">
                    <router-view></router-view>
                </div>
            </el-main>
        </el-container>

        <el-footer>All rights reserved</el-footer>
    </el-container>
</template>

<script>
import Header from "@/components/Header.vue";

export default {
    name: "app",
    components: {
        Header
    }
};
</script>

<style>
#app {
    font-family: "Helvetica Neue", Helvetica, "PingFang SC", "Hiragino Sans GB",
        "Microsoft YaHei", "微软雅黑", Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    /*text-align: center;*/
    color: #2c3e50;
}

#nav {
    padding: 30px;
}

#nav a {
    font-weight: bold;
    color: #2c3e50;
}

#nav a.router-link-exact-active {
    color: #42b983;
}

.el-header, .el-footer {
    border: 1px solid rgb(53, 48, 48)
  }
</style>

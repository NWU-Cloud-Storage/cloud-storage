<template>
    <el-container style="height: 1000px; border: 1px solid #eee">
        <el-header height="82px">
            <Header :user_info="user_info"></Header>
        </el-header>
        <el-container direction="horizontal">
            <el-aside>
                <div id="nav">
                    <el-menu>
                        <router-link to="/">
                            <el-menu-item>文件</el-menu-item>
                        </router-link>

                        <router-link to="/group-storage">
                            <el-menu-item>群组</el-menu-item>
                        </router-link>

                        <router-link to="/share/">
                            <el-menu-item>共享</el-menu-item>
                        </router-link>

                        <router-link to="/about">
                            <el-menu-item>关于</el-menu-item>
                        </router-link>
                    </el-menu>
                </div>
                <div id="info">
                    最大容量：{{ user_info.max_size }}
                    <br />
                    已用容量：{{ user_info.used_size }}
                    <br />
                    最后操作时间：{{ Date(user_info.date_last_opt) }}
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
// import Header from "@/components/Header.vue";
import Header from "./views/Header";
import axios from "axios";

export default {
    name: "app",
    components: {
        Header
    },
    data() {
        return {
            user_info: {
                username: undefined,
                nickname: undefined,
                max_size: undefined,
                used_size: undefined,
                date_last_opt: undefined
            }
        };
    },
    created() {
        console.log(this.$route.query.code);
        if (localStorage.token) {
            axios.defaults.headers.common["Authorization"] = localStorage.token;
            axios.get("/user/").catch(() => {
                this.login();
            });
        } else {
            this.login();
        }
    },
    mounted() {
        axios.get("/user/").then(response => {
            this.user_info = response.data;
        });
    },
    methods: {
        login() {
            if (this.$route.query.code) {
                let code = this.$route.query.code;
                axios.post("/login/" + code + "/").then(response => {
                    localStorage.token = response.data.token;
                    location.reload();
                });
            } else {
                window.location.href =
                    "http://authserver.nwu.edu.cn/authserver/oauth2.0/authorize?client_id=sfxzTU6D&redirect_uri=http://localhost/&state=nwu&scope=all&response_type=code";
            }
        }
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

.el-header,
.el-footer {
    border: 1px solid rgb(53, 48, 48);
    padding: 0px;
}
</style>

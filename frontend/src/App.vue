<template>
    <div  >
        <el-header height="82px" style="border: 1px solid #eee;">
            <Header :user_info="user_info"></Header>
        </el-header>
        <el-container direction="horizontal" style="">
            <el-aside style="position:relative;border: 1px solid #eee;">
                <div id="nav">
                    <el-menu style="background:#00000000">
                        <router-link to="/">
                            <el-menu-item index="1">
                                <i class="el-icon-files"></i>文件
                            </el-menu-item>
                        </router-link>
                        
                        <router-link to="/group-storage">
                            <el-menu-item index="2">
                                <i class="el-icon-user"></i>群组
                            </el-menu-item>
                        </router-link>

                        <router-link to="/share/">
                            <el-menu-item index="3">
                                <i class="el-icon-menu"></i>共享
                            </el-menu-item>
                        </router-link>

                        <router-link to="/about">
                            <el-menu-item index="4">
                                <i class="el-icon-menu"></i>关于
                            </el-menu-item>
                        </router-link>

                    </el-menu>
                </div>
                <div id="info" style="position:absolute;bottom:20px">
                    <el-card shadow="never" style="width:250px;margin-left:10px">
                        <el-progress :text-inside="true" :stroke-width="26" :percentage="percentage"></el-progress>
                        已用容量: {{ (this.user_info.used_size/1024/1024/1024).toFixed(2) + 'GB'
                                    + '/' + (this.user_info.max_size/1024/1024/1024).toFixed(2) + 'GB' }}
                    </el-card>
                    
                    <!-- {{ user_info.username }}
                    <br />
                    {{ user_info.nickname }}
                    <br />
                    最大容量：{{ user_info.max_size }}
                    <br />
                    已用容量：{{ user_info.used_size }} -->
                </div>
            </el-aside>
            <el-main style="background: #f0f0f0;">
                <div id="app" class="container" style="min-height:700px">
                    <router-view></router-view>
                </div>
            </el-main>
        </el-container>

        <el-footer style="padding:2px">
            <div style="font-size: 14px;color: #999;">
                最后操作时间：{{ Date(user_info.date_last_opt )}}
            </div>
        </el-footer>
    </div>
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
                max_size: 5368709120,
                used_size: 0,
                date_last_opt: undefined
            }
        };
    },
    computed: {
        percentage: function () {
            return Math.round(this.user_info.used_size/this.user_info.max_size * 100)
        }
    },
    created() {
        // console.log(this.$route.query.code);
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
        },
        format() {
            return (this.user_info.used_size/1024/1024/1024).toFixed(2) + 'GB'
                + '/' + (this.user_info.max_size/1024/1024/1024).toFixed(2) + 'GB';
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

.container {
    padding: 30px;
    background: #fff;
    border: 1px solid #ddd;
    border-radius: 5px;
}

</style>

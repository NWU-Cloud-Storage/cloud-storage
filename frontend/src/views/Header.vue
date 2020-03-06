<template>
    <div id="header">
        <img alt="NWU logo" src="../assets/nwu_logo.png" style="width: 250px;" />

        <el-button
            style="float: right;margin-top:25px"
            icon="el-icon-setting"
            circle
            @click="settings_dialog_visible = true"
        ></el-button>
        <div style="float: right;font-size:10px;margin:32px">你好，{{ user_info.nickname }}</div>

        <el-dropdown style="float: right;margin-top:23px">
            <el-button icon="el-icon-user" type="primary">
                <i class="el-icon-arrow-down el-icon--right"></i>
                {{ user_info.username }}
            </el-button>
            <el-dropdown-menu slot="dropdown">
                <el-dropdown-item @click.native="logout" icon="el-icon-switch-button">退出</el-dropdown-item>
            </el-dropdown-menu>
        </el-dropdown>
        <!-- <el-dropdown style="float: right;">
            <i class="el-icon-user" id="user-icon"></i>
            <el-dropdown-menu slot="dropdown">
                <el-dropdown-item>退出</el-dropdown-item>
            </el-dropdown-menu>
        </el-dropdown>-->

        <div
            style="float: right;font-size:10px;margin:32px;color:gray"
        >Tip: {{ tips[Math.floor(Math.random()*(tips.length))] }}</div>

        <el-dialog title="提示" :visible.sync="settings_dialog_visible" width="30%">
            <span>设置</span>
        </el-dialog>
    </div>
</template>

<script>
import axios from "axios";
import router from "../router/index.js"

export default {
    name: "Header",
    props: ["user_info"],
    data() {
        return {
            settings_dialog_visible: false,
            tips: [
                "可以设置分享时限为无限制",
                "群组名是可以更改的",
                "申请加入群组需要知道群组id",
                "可以对文件进行拷贝、移动、重命名等操作",
                "群组成员都可以对群文件管理"
            ]
        };
    },
    methods: {
        settings() {},
        logout() {
            axios.post("/logout/").then(() => {
                this.$alert("登出成功。", {
                    callback: () => {
                        router.push('/')
                        location.href = "http://authserver.nwu.edu.cn/authserver/logout"
                    }
                });
            });
        }
    }
};
</script>

<style>
#header {
    font: 30px Extra large;
}

#user-icon {
    font-size: 2rem;
}
</style>
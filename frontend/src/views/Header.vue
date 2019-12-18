<template>
    <div id="header">
        <img alt="NWU logo" src="../assets/nwu_logo.png" style="width: 300px;" />
        

        

        <el-button style="float: right;" icon="el-icon-setting" circle @click="settings_dialog_visible = true"></el-button>

        <div id="welcome" style="float: right;">
            {{ user_info.username }}
            {{ user_info.nickname }}
        </div>

        <el-dropdown style="float: right;">
            <el-button icon="el-icon-user" type="primary"><i class="el-icon-arrow-down el-icon--right"></i></el-button>
            <el-dropdown-menu slot="dropdown">
                <el-dropdown-item divided icon="el-icon-switch-button">退出</el-dropdown-item>
            </el-dropdown-menu>
        </el-dropdown>
        <!-- <el-dropdown style="float: right;">
            <i class="el-icon-user" id="user-icon"></i>
            <el-dropdown-menu slot="dropdown">
                <el-dropdown-item>退出</el-dropdown-item>
            </el-dropdown-menu>
        </el-dropdown>-->

        <el-dialog title="提示" :visible.sync="settings_dialog_visible" width="30%">
            <span>设置</span>
        </el-dialog>
    </div>
</template>

<script>
export default {
    name: "Header",
    props: ["user_info"],
    data() {
        return {
            settings_dialog_visible: false
        };
    },
    methods: {
        settings() {}
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
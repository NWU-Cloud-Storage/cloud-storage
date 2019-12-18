<template>
    <div id="header">
        <img alt="NWU logo" src="../assets/nwu_logo.png" style="width: 300px;" />

        <el-dropdown style="float: right;">
            <el-button icon="el-icon-user" circle></el-button>
            <el-dropdown-menu slot="dropdown">
                <el-dropdown-item>退出</el-dropdown-item>
            </el-dropdown-menu>
        </el-dropdown>

        <el-button style="float: right;" icon="el-icon-setting" circle @click="settings_dialog_visible = true"></el-button>

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
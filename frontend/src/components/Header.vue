<template>
    <div id="header">
        <img alt="NWU logo" src="../assets/nwu_logo.png" style="width: 300px;"/>
        <el-dropdown style="float: right;">
            <i class="el-icon-user" id="user-icon"></i>
            <!-- <span class="el-dropdown-link">
                <i class="el-icon-arrow-down el-icon--right el-icon-user"></i>
            </span> -->
            <el-dropdown-menu slot="dropdown">
                <el-dropdown-item>退出</el-dropdown-item>
            </el-dropdown-menu>
        </el-dropdown>
    </div>
</template>

<script>
export default {
    name: "Header"
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
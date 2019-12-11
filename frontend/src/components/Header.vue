<template>
    <div id="header">
        Northwest University Cloud Storage
        <el-dropdown>
            <i class="el-icon-user"></i>
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
.el-dropdown {
    right: 5%;
}
</style>
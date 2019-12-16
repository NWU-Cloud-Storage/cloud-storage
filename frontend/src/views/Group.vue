<template>
    <div id="group">
        <el-button type="primary" @click="create_group">建立新群组</el-button>
        <el-table
            ref="fileTable"
            :data="groups"
            style="width: 100%"
            @selection-change="handleSelectionChange"
            @row-click="toggleSelection"
            @cell-click="handleCellClick"
        >
            <el-table-column width="50" type="selection"></el-table-column>
            <el-table-column prop="name" label="名称" width="280" column-key="fileName">
                <template v-slot="slotProps">
                    <el-link
                        @click.native="handle_file_click(slotProps.$index)"
                    >{{ slotProps.row.name }}</el-link>
                    <!-- {{ tableData[slotProps.$index].id }} -->
                </template>
            </el-table-column>
            <el-table-column prop="num_of_members" label="人数" width="180"></el-table-column>
            <el-table-column prop="permission" label="权限" width="180"></el-table-column>
        </el-table>
    </div>
</template>

<script>
import axios from "axios";

export default {
    data() {
        return {
            groups: []
        };
    },
    created() {
        this.fetch_groups();
    },
    methods: {
        fetch_groups() {
            axios.get("/my-group/").then(response => {
                this.groups = response.data;
            });
        },
        create_group() {
            axios.post("/my-group/").then(response => {
                this.$message.success("成功");
            });
        }
    }
};
</script>
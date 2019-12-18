<template>
    <div id="file-list">
        <el-breadcrumb separator-class="el-icon-arrow-right" id="fileNav">
            <el-breadcrumb-item
                v-for="i in breadcrumbs"
                :key="i.id"
                :to="api_base + '/' + i.id + '/'"
            >{{ i.name }}</el-breadcrumb-item>
        </el-breadcrumb>

        <div v-if="loading" class="loading">Loading...</div>

        <div v-else class="content">
            <el-table
                ref="fileTable"
                :data="tableData"
                style="width: 100%"
                @selection-change="handleSelectionChange"
                @row-click="toggleSelection"
                @row-dblclick="handle_file_click"
            >
                <el-table-column width="50" type="selection"></el-table-column>
                <el-table-column width="50" prop="is_file">
                    <template v-slot:header>
                        <i class="el-icon-files"></i>
                    </template>
                    <template v-slot:="slotProps">
                        <i v-if="slotProps.row.is_file" class="el-icon-document"></i>
                        <i v-else class="el-icon-folder" />
                        <!-- {{ slotProps.row.isDirectory }} -->
                    </template>
                </el-table-column>
                <el-table-column prop="name" label="名称" width="280" column-key="fileName">
                    <template v-slot="slotProps">
                        <el-link
                            @click.native="handle_file_click(slotProps.row)"
                        >{{ slotProps.row.name }}</el-link>
                        <!-- {{ tableData[slotProps.$index].id }} -->
                    </template>
                </el-table-column>
                <el-table-column label="修改时间" width="180">
                    <template v-slot="scope">
                        {{ Date(scope.row.date_modified) }}
                    </template>
                </el-table-column>
                <el-table-column prop="is_shared" label="共享" width="180">
                    <template scope="scope">
                        <p>{{ scope.row.is_shared ? "是" : "否" }}</p>
                    </template>
                </el-table-column>
                <el-table-column prop="size" label="大小"></el-table-column>
            </el-table>
        </div>
        <!-- {{ $route.params.id }} -->
    </div>
</template>

<script>
import axios from "axios";
import router from "../../router/index.js";

export default {
    props: ["id", "api_base", "current_folder_api_path"],
    created() {
        this.fetch_data();
    },
    watch: {
        id() {
            this.fetch_data();
        }
    },
    data() {
        return {
            loading: false,
            selected_file: [], // 选中的文件
            tableData: [],
            breadcrumbs: []
        };
    },
    methods: {
        fetch_data() {
            this.loading = true;
            axios
                .get(this.current_folder_api_path)
                .then(response => {
                    this.tableData = response.data.content;
                    this.breadcrumbs = response.data.breadcrumbs;
                    this.loading = false;
                    console.log(response);
                    this.$emit("load-complete");
                })
                .catch(error => console.log(error));
        },
        toggleSelection(row, column, event) {
            console.log(row, column, event);
            this.$refs.fileTable.clearSelection();
            this.$refs.fileTable.toggleRowSelection(row);
        },
        handleSelectionChange(val) {
            this.selected_file = val;
            this.$emit("selected-file-change", this.selected_file);
        },
        handleCellClick(row, column, cell, event) {
            console.log(cell);
        },
        handle_file_click(row) {
            // let file = this.tableData[index];
            // console.log(this.tableData[index].id);
            if (row.is_file == false) {
                router.push({ path: this.api_base + '/' + row.id + '/'})
                // router.push({ name: "File", params: { id: file.id } });
            }
        }
    }
};
</script>

<style>
#fileNav {
    font: 25px bold;
}

</style>
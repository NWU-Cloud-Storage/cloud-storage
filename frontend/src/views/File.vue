 <template>
    <div id="file">
        <div v-if="selected_file.length">
            <el-button>共享</el-button>
            <el-button>下载</el-button>
            <el-button @click="delete_file">删除</el-button>
            <el-button @click="treeview_dialog.visible = true, treeview_dialog.operation = 'move'">移动到</el-button>
            <el-button @click="treeview_dialog.visible = true, treeview_dialog.operation = 'copy'">复制到</el-button>
            <el-button v-if="selected_file.length == 1" @click="rename_file">重命名</el-button>

            <TreeView :operation="treeview_dialog.operation" :dialog_visible.sync="treeview_dialog.visible" :source_id="selected_file.map(a => a.id)"></TreeView>
        </div>
        <div v-else>
            <el-dropdown trigger="click">
                <el-button>
                    新建
                    <i class="el-icon-arrow-down el-icon--right"></i>
                </el-button>
                <el-dropdown-menu slot="dropdown">
                    <el-dropdown-item @click.native="new_floder">文件夹</el-dropdown-item>
                </el-dropdown-menu>
            </el-dropdown>
            <el-dropdown trigger="click">
                <el-button>
                    上传
                    <i class="el-icon-arrow-down el-icon--right"></i>
                </el-button>
                <el-dropdown-menu slot="dropdown">
                    <el-dropdown-item>文件</el-dropdown-item>
                    <el-dropdown-item>文件夹</el-dropdown-item>
                </el-dropdown-menu>
            </el-dropdown>
        </div>

        <el-breadcrumb separator-class="el-icon-arrow-right" id="fileNav">
            <el-breadcrumb-item
                v-for="i in breadcrumbs"
                :key="i.id"
                :to="{ name: 'File', params: { id: i.id }}"
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
                @cell-click="handleCellClick"
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
                            @click.native="handle_file_click(slotProps.$index)"
                        >{{ slotProps.row.name }}</el-link>
                        <!-- {{ tableData[slotProps.$index].id }} -->
                    </template>
                </el-table-column>
                <el-table-column prop="modifiedDate" label="修改时间" width="180"></el-table-column>
                <el-table-column prop="shareStatus" label="共享" width="180"></el-table-column>
                <el-table-column prop="size" label="大小"></el-table-column>
            </el-table>
        </div>
        <!-- {{ $route.params.id }} -->
    </div>
</template>

<script>
import axios from "axios";
import TreeView from "./components/TreeView.vue";
import router from "../router/index.js";

export default {
    components: {
        TreeView
    },
    data() {
        return {
            selected_file: [], // 选中的文件
            tableData: [],
            breadcrumbs: [{ id: 0, path: "/file/", name: "文件" }],
            id: undefined,
            loading: false,
            treeview_dialog: {
                visible: false,
                operation: undefined
            }
        };
    },
    created() {
        this.fetchData();
    },
    mounted() {},
    watch: {
        // 如果路由有变化，会再次执行该方法
        $route() {
            this.fetchData();
            this.selected_file.splice(0);
        }
    },
    filters: {
        size(value) {
            return value.toFixed(2);
        }
    },
    methods: {
        fetchData() {
            this.loading = true;
            console.log(this.$route.params.id);
            this.id = this.$route.params.id;
            if (this.id == undefined) {
                this.apiPath = "/api/my-storage/";
            } else {
                this.apiPath = "/api/my-storage/" + this.id + "/";
            }
            axios
                .get(this.apiPath)
                .then(response => {
                    this.tableData = response.data.content;
                    this.breadcrumbs = response.data.breadcrumbs;
                    this.loading = false;
                    console.log(response);
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
        },
        handleCellClick(row, column, cell, event) {
            console.log(cell);
        },
        filePath(index) {
            return this.$route.path + this.tableData[index].id + "/";
        },
        handle_file_click(index) {
            let file = this.tableData[index];
            console.log(this.tableData[index].id);
            if (file.is_file == false) {
                router.push({ name: "File", params: { id: file.id } });
            }
        },
        delete_file() {
            this.$confirm("此操作将永久删除该文件, 是否继续?", "提示", {
                confirmButtonText: "确定",
                cancelButtonText: "取消",
                type: "warning"
            })
                .then(() => {
                    this.$message({
                        type: "success",
                        message: "删除成功!"
                    });
                })
                .catch(() => {
                    this.$message({
                        type: "info",
                        message: "已取消删除"
                    });
                });
        },
        rename_file() {
            let id = this.selected_file[0].id;
            this.$prompt("重命名", {
                confirmButtonText: "确定",
                cancelButtonText: "取消",
                inputValue: this.selected_file[0].name,
                inputPattern: /\w/,
                inputErrorMessage: "文件名不能包含特殊字符"
            }).then(({value}) => {
                console.log(value)
                axios.put(this.apiPath, {
                    "name": value,
                })
                .then((response) => {
                    console.log(response)
                    this.$message('修改成功');
                })
                .catch((error) => {
                    console.log(error)
                    this.$message.error('出错了')
                })
            });
        },
        new_floder() {
            this.$prompt("新建", {
                inputPlaceholder: "输入您的文件夹名称",
            })
            .then(({value}) => {
                axios.post(this.apiPath, {

                })
            })
        }
    },
    computed: {}
};
</script>

<style>
#fileNav {
    font: 25px bold;
}

.fileName {
    text-decoration: underline;
}

/* .cell:hover {
    text-decoration: underline;
} */

.el-dropdown {
    vertical-align: top;
}
.el-dropdown + .el-dropdown {
    margin-left: 15px;
}
.el-icon-arrow-down {
    font-size: 12px;
}

.el-breadcrumb {
    margin: 20px 0px;
}
</style>
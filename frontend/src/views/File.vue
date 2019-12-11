 <template>
    <div id="file">
        <div v-if="selected_file.length">
            <el-button>共享</el-button>
            <el-button>下载</el-button>
            <el-button @click="delete_file">删除</el-button>
            <el-button @click="treeview_dialog.visible = true">移动到</el-button>
            <el-button>复制到</el-button>
            <el-button>重命名</el-button>

            <TreeView title="将项目移动到" :dialog_visible.sync="treeview_dialog.visible"></TreeView>
            <TreeView title="将项目复制到" :dialog_visible.sync="treeview_dialog.visible"></TreeView>

        </div>
        <div v-else>
            <el-dropdown trigger="click">
                <el-button>
                    新建
                    <i class="el-icon-arrow-down el-icon--right"></i>
                </el-button>
                <el-dropdown-menu slot="dropdown">
                    <el-dropdown-item>文件夹</el-dropdown-item>
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
                :to="i.path"
                @click.native="deleteBreadcrumb(i.id)"
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
                        <router-link
                            :to="filePath(slotProps.$index)"
                            @click.native="addBreadcrumbElement(slotProps.$index)"
                        >{{ slotProps.row.name }}</router-link>
                        <!-- {{ slotProps.$index }} -->
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

export default {
    components: {
        TreeView
    },
    data() {
        return {
            selected_file: [], // 选中的文件
            info: "",
            tableData: [],
            breadcrumbs: [{ id: 0, path: "/file/", name: "文件" }],
            path: "",
            apiPath: "",
            loading: false,
            treeview_dialog: {
                visible: false
            }
        };
    },
    created() {
        this.fetchData();
        this.setBreadcrumbFromRoute();
    },
    mounted() {},
    watch: {
        // 如果路由有变化，会再次执行该方法
        $route() {
            this.fetchData();
            this.setBreadcrumbFromRoute();
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
            this.path = "/file/" + this.$route.params.pathMatch;
            this.apiPath = "/api" + this.path;
            axios
                .get(this.apiPath)
                .then(response => {
                    this.tableData = response.data;
                    // this.info = response;
                    this.loading = false;
                    console.log(response);
                })
                .catch(error => console.log(error));
            // console.log(this.path);
            // console.log(this.$route.params.pathMatch.split("/"));
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
            return this.$route.path + this.tableData[index].name + "/";
        },
        setBreadcrumbFromRoute() {
            // ["", "file", "文件夹1", "文件夹2", ""]
            // 可能存在效率问题
            this.breadcrumbs.splice(1);
            let pathArray = this.$route.path.split("/");
            for (let i = 2; i < pathArray.length - 1; i++) {
                let path = "";
                let name = pathArray[i];
                for (let j = 0; j <= i; j++) {
                    path += pathArray[j] + "/";
                }
                this.breadcrumbs.push({
                    id: this.breadcrumbs.length,
                    path: path,
                    name: name
                });
            }
        },
        addBreadcrumbElement(index) {
            // 这个事件触发时路由已经是点击后的路由了
            // console.log(this.$route.params)
            // let path = this.$route.path;
            // let name = this.tableData[index].fileName;
            // this.breadcrumbs.push({
            //     id: this.breadcrumbs.length,
            //     path: path,
            //     name: name
            // });
        },
        deleteBreadcrumb(index) {
            // console.log(index);
            // this.breadcrumbs.splice(index+1);
        }, // 以上两个方法暂时被setBreadcrumbFromRoute替代
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
        loadNode(node, resolve) {
            if (node.level === 0) {
                return resolve([{ directory_name: "region" }]);
            }
            if (node.level > 1) return resolve([]);

            setTimeout(() => {
                const data = [
                    {
                        directory_name: "leaf"
                    },
                    {
                        directory_name: "zone"
                    }
                ];
                resolve(data);
            }, 500);
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
 <template>
    <div id="file">
        <div v-if="selected_file.length">
            <el-popover placement="bottom" width="400" trigger="click">
                过期时间
                <el-select v-model="share.duration.value" placeholder="请选择">
                    <el-option
                        v-for="item in share.duration.options"
                        :key="item.value"
                        :label="item.label"
                        :value="item.value"
                    ></el-option>
                </el-select>
                <br/>密码
                <el-switch v-model="share.password.status"></el-switch>
                <el-input placeholder="请输入内容" v-model="share.password.value" :disabled="!share.password.status"></el-input>
                <el-button @click="share_file">生成共享链接</el-button><br>
                共享链接<el-input v-model="share.share_url"></el-input>
                <el-button slot="reference" style="margin-right: 10px;">共享</el-button>
            </el-popover>
            <el-button>下载</el-button>
            <el-button @click="delete_file">删除</el-button>
            <el-button
                @click="treeview_dialog.visible = true, treeview_dialog.operation = 'move'"
            >移动到</el-button>
            <el-button
                @click="treeview_dialog.visible = true, treeview_dialog.operation = 'copy'"
            >复制到</el-button>
            <el-button v-if="selected_file.length == 1" @click="rename_file">重命名</el-button>

            <TreeView
                :operation="treeview_dialog.operation"
                :dialog_visible.sync="treeview_dialog.visible"
                :source_id="selected_file.map(a => a.id)"
            ></TreeView>
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
                    <el-dropdown-item>
                        <label for="file-upload">文件</label>
                        <input
                            type="file"
                            name="file"
                            class="upload-button"
                            id="file-upload"
                            @change="upload_file"
                        />
                    </el-dropdown-item>
                    <el-dropdown-item>
                        <label for="folder-upload">文件夹</label>
                        <input
                            type="file"
                            class="upload-button"
                            id="folder-upload"
                            webkitdirectory
                            @change="upload_file"
                        />
                    </el-dropdown-item>
                </el-dropdown-menu>
            </el-dropdown>
        </div>

        <FileList api_base="/my-storage" :id="id" @selected-file-change="handle_file_selected"></FileList>

    </div>
</template>

<script>
import TreeView from "./components/TreeView.vue";
import FileList from "./components/FileList.vue";
import axios from "axios";


export default {
    components: {
        TreeView,
        FileList
    },
    data() {
        return {
            id: undefined,
            selected_file: {
                length: 0,
            },
            treeview_dialog: {
                visible: false,
                operation: undefined
            },
            share: {},
        };
    },
    created() {
        this.id = this.$route.params.id;
    },
    mounted() {},
    watch: {
        // 如果路由有变化，会再次执行该方法
        $route() {
            this.id = this.$route.params.id;
        },
        selected_file() {
            this.share = {
                duration: {
                    options: [
                        {
                            value: 1,
                            label: "一天"
                        },
                        {
                            value: "infinite",
                            label: "永久"
                        }
                    ],
                    value: "infinite"
                },
                password: {
                    status: false,
                    value: ""
                },
                share_url: ""
            }
        }
    },
    filters: {
        size(value) {
            return value.toFixed(2);
        }
    },
    methods: {
        handle_file_selected(selected_file) {
            this.selected_file = selected_file;
        },
    
        filePath(index) {
            return this.$route.path + this.tableData[index].id + "/";
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
            // TODO input validate
            this.$prompt("重命名", {
                confirmButtonText: "确定",
                cancelButtonText: "取消",
                inputValue: this.selected_file[0].name,
                inputPattern: /\w/,
                inputErrorMessage: "文件名不能包含特殊字符"
            })
                .then(({ value }) => {
                    console.log(value);
                    axios
                        .put('/my-storage/' + id + '/', {
                            name: value
                        })
                        .then(response => {
                            console.log(response);
                            this.$message("修改成功");
                        })
                        .catch(error => {
                            console.log(error);
                            this.$message.error("出错了");
                        });
                })
                .catch(error => {
                    console.log(error);
                });
        },
        new_floder() {
            this.$prompt("新建", {
                inputPlaceholder: "输入您的文件夹名称"
            }).then(({ value }) => {
                axios.post('/my-storage/', {
                    name: value
                }).then(response => {
                    this.$message.success("成功");
                });
            });
        },
        upload_file(e) {
            let formData = new FormData();
            let data = JSON.stringify({
                base_folder_id: this.id
            });
            formData.append("file", e.target.files[0]);
            formData.append("data", data); // 上传文件的同时， 也可以上传其他数据

            axios
                .post("/api/upload/", formData, {
                    headers: { "Content-Type": "multipart/form-data" }
                })
                .then(response => {
                    console.log(response);
                })
                .catch(error => {
                    console.log(error);
                });
        },
        share_file() {
            axios.post('/share-to-public/' + this.selected_file[0].id + '/', {
                duration: this.share.duration.value,
                password: this.share.password.value
            }).then(response => {
                this.share.share_url = response.data.url;
            })
        }
    },
    computed: {}
};
</script>

<style>

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

.upload-button {
    display: none;
}

.el-button {
    margin-left: 10px;
}
</style>
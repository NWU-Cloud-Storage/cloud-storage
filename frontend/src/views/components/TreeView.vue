<template>
    <el-dialog :title="title" :visible.sync="visible" width="30%">
        <el-tree ref="tree" :props="properties" :load="loadNode" lazy></el-tree>
        <span slot="footer" class="dialog-footer">
            <el-button @click="visible = false">取 消</el-button>
            <el-button type="primary" @click="submit">确 定</el-button>
        </span>
    </el-dialog>
</template>

<script>
import axios from "axios";

export default {
    name: "file-to",
    props: ["dialog_visible", "operation", "source_id"],
    data() {
        return {
            properties: {
                label: "name",
                children: "zones",
                isLeaf: "is_file"
            }
        };
    },
    computed: {
        visible: {
            get() {
                return this.dialog_visible;
            },
            set(newVal) {
                this.$emit("update:dialog_visible", newVal);
            }
        },
        title() {
            if (this.operation == "move") {
                return "移动到";
            } else {
                return "复制到";
            }
        }
    },
    created() {},
    watch: {
        visible() {
            // console.log(this.source_id)
        }
    },
    methods: {
        loadNode(node, resolve) {
            let apiPath;
            //第0层的node没有id
            if (node.level === 0) {
                resolve([{ name: "文件" }]);
            } else {
                if (node.level === 1) {
                    apiPath = "/my-storage/";
                } else {
                    let id = node.data.id;
                    console.log(node.data.id);
                    apiPath = "/my-storage/" + id + "/";
                }
                axios
                    .get(apiPath)
                    .then(response => {
                        let data = response.data.content;
                        let res = [];
                        for (let i in data) {
                            if (data[i].is_file === false) {
                                res.push(data[i]);
                            }
                        }
                        resolve(res);
                        // console.log(node);
                    })
                    .catch(error => console.log(error));
            }
        },
        submit() {
            console.log(this.$refs.tree.getCurrentNode());
            // 不点击任何一个文件夹时的行为
            if (this.$refs.tree.getCurrentNode() === null) {
                this.$message.warning("请选择一个文件夹");
            } else {
                axios
                    .put("/my-storage/" + this.operation + "/", {
                        source_id: this.source_id,
                        destination_id: this.$refs.tree.getCurrentNode().id
                    })
                    .then(response => {
                        this.$message.success("成功");
                        this.$emit("update_data");
                    })
                    .catch(error => {
                        this.$message.error(error);
                        console.log(error);
                    });
                this.visible = false;
            }
        }
    }
};
</script>

<style>
</style>
<template>
    <el-dialog :title="title" :visible.sync="dialog_visible" width="30%">
        <el-tree :props="props" :load="loadNode" lazy></el-tree>
        <span slot="footer" class="dialog-footer">
            <el-button @click="dialog_visible = false">取 消</el-button>
            <el-button type="primary" @click="dialog_visible = false">确 定</el-button>
        </span>
    </el-dialog>
</template>

<script>
export default {
    name: "file-to",
    props: ["title"],
    inject: ['dialog_visible'],
    data() {
        return {
            props: {
                label: "directory_name",
                children: "zones",
                isLeaf: "leaf"
            }
        };
    },
    // computed: {
    //     dialog_visible: () => {
    //         console.log(this.$parent.dialog_visible)
    //         return this.$parent.dialog_visible
    //     }
    // },
    created() {
        console.log(this.$parent.dialog_visible);

    },
    methods: {
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
    }
};
</script>

<style>
</style>
<template>
    <div id="shared-files-view">
        <div v-if="selected_file.length">
            <el-button @click="treeview_dialog_visible = true">保存至我的仓库</el-button>

            <TreeView
                operation="copy"
                :dialog_visible.sync="treeview_dialog_visible"
                :source_id="selected_file.map(a => a.id)"
            ></TreeView>
        </div>
        <FileList :api_base="'/share/' + share_id" :id="id" @selected-file-change="handle_file_selected"></FileList>
    </div>
</template>

<script>
import FileList from "./components/FileList";
import TreeView from "./components/TreeView";

export default {
    components: {
        FileList,
        TreeView
    },
    data() {
        return {
            id: undefined,
            share_id: undefined,
            treeview_dialog_visible: false,
            selected_file: [],
        }
    },
    created() {
        this.share_id = this.$route.params.share_id;
    },
    methods: {
        handle_file_selected(selected_file) {
            this.selected_file = selected_file;
        },
    }
}
</script>
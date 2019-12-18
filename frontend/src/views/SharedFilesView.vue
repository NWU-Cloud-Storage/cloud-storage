<template>
    <div id="shared-files-view">
        <FileList :api_base="'/share/' + share_id" :id="id" @selected-file-change="handle_file_selected"></FileList>
    </div>
</template>

<script>
import FileList from "./components/FileList.vue";

export default {
    components: {
        FileList
    },
    data() {
        return {
            id: undefined,
            share_id: undefined
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
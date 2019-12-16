<template>
    <div id="shared-files-view">
        <FileList :api_base="'/share/' + share_id + '/'" :id="id" @selected-file-change="handle_file_selected"></FileList>
    </div>
</template>

<script>
export default {
    data() {
        return {
            id: undefined,
            share_id: undefined
        }
    },
    created() {
        this.share_id = this.$route.params.share_id;
    }
}
</script>
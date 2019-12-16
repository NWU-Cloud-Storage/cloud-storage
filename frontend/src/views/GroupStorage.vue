<template>
    <div id="group_file">
        <File :api_base="'/group-storage/' + this.$route.params.group_id"></File>
    </div>
</template>

<script>
import File from "./components/File";

export default {
    components: {
        File
    }

}
</script>
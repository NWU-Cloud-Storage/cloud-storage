<template>
    <div id="my-storage">
        <File @uploading="handle_upload_progress" api_base="/my-storage"></File>

        <div class="loading" v-if="loading">
            <span class="tips">上传进度</span>
            <!--进度条-->
            <el-progress type="line" :percentage="percentage" class="progress" :show-text="true"></el-progress>
        </div>
    </div>
</template>

<script>
import File from "./components/File";

export default {
    components: {
        File
    },
    mounted() {},
    data() {
        return {
            percentage: 0,
            loading: false
        };
    },
    methods: {
        handle_upload_progress(progressEvent) {
            this.loading = true
            console.log(progressEvent);
            this.percentage = (progressEvent.loaded / progressEvent.total ).toFixed(2) * 100
            if (progressEvent.loaded == progressEvent.total) {
                this.loading = false
                this.$message.success("上传成功")
            }
        },
        format(percentage) {
            return 'asdfasdf'
        }
    }
};
</script>

<style>
.loading {
    position: fixed;
    top: 0;
    right: 0;
    left: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.8);
}
.progress {
    width: 300px;
    height: 200px;
    position: absolute;
    top: 50%;
    left: 50%;
    margin-left: -100px;
    margin-top: -100px;
}
.tips {
    color: #cbcbcc;
    position: absolute;
    top: 50%;
    left: 50%;
    margin-left: -100px;
    margin-top: -150px;
}
</style>
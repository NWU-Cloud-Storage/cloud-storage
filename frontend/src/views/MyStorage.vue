<template>
    <div id="my-storage">
        <File @uploading="handle_upload_progress" api_base="/my-storage" name="my-storage"></File>

        <div id="upload-loading" v-if="loading">
            <span class="tips">上传进度</span>
            <!--进度条-->
            <el-progress type="line" :percentage="percentage" class="progress" :show-text="true" :format="format"></el-progress>
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
            loading: false,
            last_time_stamp: 0,
            last_loaded: 0,
            total: 0,
            speed: 0,
        };
    },
    methods: {
        handle_upload_progress(progressEvent) {
            this.loading = true
            // console.log(progressEvent);
            this.speed = (progressEvent.loaded - this.last_loaded) / (progressEvent.timeStamp - this.last_time_stamp) * 1000
            // console.log(this.last_loaded, this.last_time_stamp, this.speed)
            this.last_time_stamp = progressEvent.timeStamp
            this.last_loaded = progressEvent.loaded
            // console.log(this.last_loaded, this.last_time_stamp)

            this.percentage = (progressEvent.loaded / progressEvent.total ).toFixed(2) * 100
            if (progressEvent.loaded == progressEvent.total) {
                this.loading = false
                this.$message.success("上传成功")
            }
        },
        format(percentage) {
            let dimensions = ["B", "KB", "MB", "GB"];
            let size = this.speed;

            for (let i in dimensions) {
                if (size >= 1024) {
                    size /= 1024;
                } else {
                    return size.toFixed(2) + dimensions[i] + "/s";
                }
            }
            return size.toFixed(2) + dimensions[3];
        }
    }
};
</script>

<style>
#upload-loading {
    position: fixed;
    top: 0;
    right: 0;
    left: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.8) !important;
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
 <template>
    <div id="file">
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
                <el-table-column width="50" prop="isDirectory">
                    <template v-slot:header>
                        <i class="el-icon-files"></i>
                    </template>
                    <template v-slot:="slotProps">
                        <i v-if="slotProps.row.isDirectory" class="el-icon-folder"></i>
                        <i v-else class="el-icon-document" />
                        <!-- {{ slotProps.row.isDirectory }} -->
                    </template>
                </el-table-column>
                <el-table-column prop="fileName" label="名称" width="180" column-key="fileName">
                    <template v-slot="slotProps">
                        <router-link
                            :to="filePath(slotProps.$index)"
                            @click.native="addBreadcrumbElement(slotProps.$index)"
                        >{{ slotProps.row.fileName }}</router-link>
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

export default {
    data() {
        return {
            checked: [],
            info: "",
            tableData: [],
            breadcrumbs: [{ id: 0, path: "/file/", name: "文件" }],
            path: "",
            apiPath: "",
            loading: false
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
                    this.tableData = response.data.data;
                    // this.info = response;
                    this.loading = false;
                })
                .catch(error => console.log(error));
            // console.log(this.path);
            // console.log(this.$route.params.pathMatch.split("/"));
        },
        toggleSelection(row, column, event) {
            console.log(row, column, event);
            this.$refs.fileTable.toggleRowSelection(row);
        },
        handleSelectionChange(val) {
            this.checked = val;
        },
        handleCellClick(row, column, cell, event) {
            console.log(cell);
        },
        filePath(index) {
            return this.$route.path + this.tableData[index].fileName + "/";
        },
        setBreadcrumbFromRoute() {
            // ["", "file", "文件夹1", "文件夹2", ""]
            // 可能存在效率问题
            this.breadcrumbs.splice(1);
            let pathArray = this.$route.path.split('/');
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
        } // 以上两个方法暂时被setBreadcrumbFromRoute替代
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
</style>
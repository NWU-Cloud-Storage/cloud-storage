 <template>
    <div id="file">
        <el-breadcrumb separator-class="el-icon-arrow-right" id="fileNav">
            <el-breadcrumb-item :to="{ path: '/file/' }">文件</el-breadcrumb-item>
        </el-breadcrumb>

        <el-table
            ref="fileTable"
            :data="tableData"
            style="width: 100%"
            @selection-change="handleSelectionChange"
            @row-click="toggleSelection"
        >
            <el-table-column width="50" type="selection"></el-table-column>
            <el-table-column width="50" prop="isDirectory">
                <template v-slot:header>
                    <i class="el-icon-files"></i>
                </template>
                <template v-slot:="slotProps">
                    <i v-if="slotProps.row.isDirectory" class="el-icon-folder"></i>
                    <i v-else class="el-icon-document"/>
                    <!-- {{ slotProps.row.isDirectory }} -->
                </template>
                
            </el-table-column>
            <el-table-column prop="fileName" label="名称" width="180" column-key="fileName">
                <template v-slot="slotProps">
                    <!-- <router-link>{{ slotProps.row.fileName }}<router-link> -->
                    <a :href="slotProps.row.fileName">{{ slotProps.row.fileName }}</a>
                    <!-- {{ slotProps.column }} -->
                </template>
            </el-table-column>
            <el-table-column prop="modifiedDate" label="修改时间" width="180"></el-table-column>
            <el-table-column prop="shareStatus" label="共享" width="180"></el-table-column>
            <el-table-column prop="size" label="大小"></el-table-column>
        </el-table>
        {{ $route.params.id }}
    </div>
</template>

<script>
import axios from "axios";

export default {
    data() {
        return {
            checked: [],
            info: "",
            tableData: []
        };
    },
    mounted() {
        axios
            .get("/api/data")
            .then(
                response => (
                    (this.tableData = response.data.data),
                    (this.info = response)
                )
            )
            .catch(error => console.log(error));
            console.log(this.$route.params);
        console.log(this.$route.params.pathMatch.split('/'));
    },
    filters: {
        size(value) {
            return value.toFixed(2);
        }
    },
    methods: {
        toggleSelection(row, column, event) {
            console.log(row, column, event);
            this.$refs.fileTable.toggleRowSelection(row);
        },
        handleSelectionChange(val) {
            this.checked = val;
        }
    }
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
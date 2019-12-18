<template>
    <div id="group">
        <el-button type="primary" @click="create_group">建立新群组</el-button>
        <el-button type="primary" @click="join_group">申请加群</el-button>
        <el-table ref="fileTable" :data="groups" style="width: 100%">
            <el-table-column width="50" type="selection"></el-table-column>
            <el-table-column prop="name" label="名称" width="280" column-key="fileName">
                <template v-slot="slotProps">
                    <el-link
                        @click.native="handle_group_click(slotProps.$index)"
                    >{{ slotProps.row.name }}</el-link>
                    <!-- {{ tableData[slotProps.$index].id }} -->
                </template>
            </el-table-column>
            <el-table-column prop="id" label="ID" width="80"></el-table-column>
            <el-table-column prop="num_of_members" label="人数" width="80"></el-table-column>
            <el-table-column label="权限" width="80">
                <template v-slot="scope">{{ scope.row.permission === "master" ? "群主" : "成员" }}</template>
            </el-table-column>
            <el-table-column label="操作">
                <template slot-scope="scope">
                    <el-button
                        size="mini"
                        type="info"
                        @click="detail_table_visible = true, fetch_group_detail(scope.row.id)"
                    >查看人员</el-button>
                    <el-button
                        size="mini"
                        type="primary"
                        @click="apply_table_visible = true,fetch_apply_detail(scope.row.id)"
                    >查看加群列表</el-button>
                    <el-button size="mini" @click="change_group_name(scope.row.id)">修改名称</el-button>
                    <el-button
                        size="mini"
                        type="danger"
                        @click="exit_or_delete_group(scope.row)"
                    >退出/解散</el-button>
                </template>
            </el-table-column>
        </el-table>

        <el-dialog title="人员" :visible.sync="detail_table_visible">
            <el-table :data="detail_table_data">
                <el-table-column property="username" label="学号" width="150"></el-table-column>
                <el-table-column property="nickname" label="昵称" width="200"></el-table-column>
                <el-table-column property="permission" label="权限"></el-table-column>
                <el-table-column label="操作">
                    <template slot-scope="scope">
                        <el-button size="mini" type="danger" @click="delete_member(scope.row)">删除</el-button>
                    </template>
                </el-table-column>
            </el-table>
        </el-dialog>

        <el-dialog title="加群列表" :visible.sync="apply_table_visible">
            <el-table :data="apply_table_data">
                <el-table-column property="username" label="学号" width="150"></el-table-column>
                <el-table-column property="nickname" label="昵称" width="200"></el-table-column>
                <el-table-column property="date_intented" label="申请时间"></el-table-column>
                <el-table-column label="操作">
                    <template slot-scope="scope">
                        <el-button size="mini" type="success" @click="agree_apply(scope.row)">同意</el-button>
                        <el-button size="mini" type="danger" @click="deny_apply(scope.row)">拒绝</el-button>
                    </template>
                </el-table-column>
            </el-table>
        </el-dialog>
    </div>
</template>

<script>
import axios from "axios";
import router from "../router/index.js";

export default {
    data() {
        return {
            groups: [],
            detail_table_visible: false,
            detail_table_data: [],
            apply_table_data: [],
            current_group_id: undefined
        };
    },
    created() {
        this.fetch_groups();
    },
    methods: {
        fetch_groups() {
            axios.get("/my-group/").then(response => {
                this.groups = response.data;
            });
        },
        fetch_group_detail(id) {
            this.current_group_id = id;
            axios.get("/my-group/" + id + "/").then(response => {
                this.detail_table_data = response.data.members;
            });
        },
        fetch_apply_detail(id) {
            this.current_group_id = id;
            axios.get("/intention/" + id + "/").then(response => {
                this.apply_table_data = response.data;
            });
        },
        create_group() {
            this.$prompt("请输入群组名称")
                .then(({ value }) => {
                    return axios.post("/my-group/", {
                        name: value
                    });
                })
                .then(response => {
                    this.$message.success("成功");
                    this.fetch_groups();
                });
        },
        handle_group_click(index) {
            let group = this.groups[index];
            console.log(this.groups[index].id);
            // router.push({
            //     name: "GroupStorage",
            //     params: { group_id: group.id }
            // });
            router.push({ path: "/group-storage/" + group.id + "/" });
        },
        change_group_name(id) {
            this.$prompt("请输入新的群组名称")
                .then(({ value }) => {
                    return axios.put("/my-group/" + id + "/", {
                        name: value
                    });
                })
                .then(response => {
                    this.$message.success("修改成功");
                    this.fetch_groups();
                });
        },
        exit_or_delete_group(row) {
            console.log(row);
            let prompt = row.permission == "master" ? "解散" : "退出";
            this.$confirm("您将" + prompt + "该群组,是否继续?", {
                type: "warning"
            })
                .then(() => {
                    return axios.delete("/my-group/" + row.id + "/");
                })
                .then(response => {
                    this.$message.success("成功");
                    this.fetch_groups();
                });
        },
        delete_member(row) {
            this.$confirm("您将移除" + row.username + ",是否继续?", {
                type: "warning"
            })
                .then(() => {
                    return axios.delete(
                        "/membership/" +
                            this.current_group_id +
                            "/" +
                            row.username +
                            "/"
                    );
                })
                .then(response => {
                    this.$message.success("成功");
                    this.fetch_groups();
                });
        },
        agree_apply(row) {
            axios
                .post(
                    "/intention/" +
                        this.current_group_id +
                        "/" +
                        row.username +
                        "/"
                )
                .then(response => {
                    this.$message.success("同意成功");
                });
        },
        deny_apply(row) {
            axios
                .delete(
                    "/intention/" +
                        this.current_group_id +
                        "/" +
                        row.username +
                        "/"
                )
                .then(response => {
                    this.$message.success("拒绝成功");
                });
        },
        join_group() {
            this.$prompt("请输入要加入群组的id")
                .then(({ value }) => {
                    return axios.post("/intention/" + value + "/");
                })
                .then(response => {
                    this.$message.success("申请成功");
                }); ``
        }
    }
};
</script>
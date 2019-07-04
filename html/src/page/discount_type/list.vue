<template>
  <div class="main">
    <!--功能区-->
    <div class="banner">
      <router-link to="/discount/type/add">
        <el-button size="medium" type="primary">新增</el-button>
      </router-link>
    </div>
    <!--数据列表-->
    <el-table
      :data="table_data"
      style="width: 100%">
      <el-table-column
        align="center"
        label="类型">
        <template slot-scope="scope">
          <el-input v-if="cur_index == scope.row.id" v-model="scope.row.type" placeholder="类型"></el-input>
          <span v-else>{{ scope.row.type }}</span>
        </template>
      </el-table-column>
      <el-table-column
        align="center"
        prop="name"
        label="名称">
        <template slot-scope="scope">
          <el-input v-if="cur_index == scope.row.id" v-model="scope.row.name" placeholder="名称"></el-input>
          <span v-else>{{ scope.row.name }}</span>
        </template>
      </el-table-column>
      <el-table-column
        fixed="right"
        min-width="95"
        label="操作">
        <template slot-scope="scope">
          <div v-if="cur_index == scope.row.id">
            <el-button
              @click="handleSave(scope.row)"
              type="text" size="small">保存
            </el-button>
            <el-button
              @click="handleCancel(scope.row)"
              type="text" size="small">取消
            </el-button>
          </div>
          <div v-else>
            <el-button
              @click="handleEdit(scope.row)"
              type="text">修改
            </el-button>
            <el-button
              @click="handleDelete(scope.row)"
              type="text">删除
            </el-button>
          </div>
        </template>
      </el-table-column>
    </el-table>
    <!--分页-->
    <div class="footer">
      <el-pagination
        background
        :page-size="page_size"
        layout="prev, pager, next"
        :total="total"
        @current-change="currentChange">
      </el-pagination>
    </div>
  </div>
</template>

<script>
  export default {
    data () {
      return {
        cur_index: -1,
        last_type: '',
        last_name: '',
        table_data: [],
        cur_page: 1,
        page_size: 0,
        total: 0
      }
    },
    created () {
      this.getData();
    },
    methods: {
      getData (cur_page = 1) {
        let params = {
          cur_page: cur_page
        }
        this.$axios.get('/api/admin/discount/type', {params: params})
          .then((res) => {
            this.table_data = res.data.data;
            this.page_size = res.data.page_size;
            this.total = res.data.total;
          })
          .catch((err) => {
            console.log(err);
          })
      },
      handleSave (row) {
        let data = new FormData();
        data.append('id', row.id);
        data.append('type', row.type);
        data.append('name', row.name);
        this.$axios.put('/api/admin/discount/type', data)
          .then((res) => {
            if (!res.data.code) {
              this.cur_index = -1;
              this.$message({
                message: res.data.msg,
                type: 'success',
                showClose: true
              });
            } else {
              this.$message({
                message: res.data.msg,
                type: 'error',
                showClose: true
              });
            }
          })
          .catch((err) => {
            console.log(err);
          });
      },
      handleCancel (row) {
        this.table_data.map((data) => {
          if (data.id == row.id) {
            data.type = this.last_type;
            data.name = this.last_name;
          }
        });
        this.cur_index = -1;
        this.$message({
          type: 'info',
          message: '已取消',
          showClose: true
        });
      },
      handleEdit (row) {
        if (this.cur_index != -1) {
          this.$message({
            message: '请保存或取消！',
            type: 'warning',
            showClose: true
          });
          return;
        }
        this.last_type = row.type;
        this.last_name = row.name;
        this.cur_index = row.id;
      },
      handleDelete (row) {
        this.$confirm('此操作将永久删除该优惠券类型, 是否继续?', '提示', {
          cancelButtonText: '取消',
          confirmButtonText: '确定',
          type: 'warning',
          center: true
        }).then(() => {
          let data = new FormData();
          data.append('id', row.id);
          this.$axios.delete('/api/admin/discount/type', {data: data})
            .then((res) => {
              if (!res.data.code) {
                if (this.cur_page > 1 && this.table_data.length <= ((this.cur_page - 1) * this.page_size) + 1) {
                  this.cur_page = this.cur_page - 1;
                }
                this.getData(this.cur_page);
                this.$message({
                  type: 'success',
                  message: res.data.msg,
                  showClose: true
                });
              } else {
                this.$message({
                  message: res.data.msg,
                  type: 'error',
                  showClose: true
                });
              }
            })
            .catch((err) => {
              console.log(err);
            });
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消删除'
          });
        });
      },
      currentChange (cur_page) {
        this.cur_page = cur_page;
        this.getData(cur_page);
      }
    }
  }
</script>

<style scoped>
  .main {
    padding: 12px;
  }

  .banner {
    margin-bottom: 12px;
    padding: 10px;
    background: #ffffff;
  }

  .footer {
    margin-top: 12px;
    margin-bottom: 12px;
    padding: 10px;
    text-align: center;
    background: #ffffff;
  }
</style>

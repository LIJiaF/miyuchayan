<template>
  <div class="main">
    <!--功能区-->
    <div class="banner">
      <el-row type="flex" :gutter="10" align="middle">
        <el-col :span="8">
          <el-input
            placeholder="搜索微信号"
            prefix-icon="el-icon-search"
            v-model="search_val">
          </el-input>
        </el-col>
        <el-col :span="4">
          <el-button @click="handleSearch" size="medium" type="primary">搜索</el-button>
        </el-col>
      </el-row>
    </div>
    <!--数据列表-->
    <el-table
      :data="table_data"
      style="width: 100%">
      <el-table-column
        align="center"
        fixed="left"
        label="头像">
        <template slot-scope="scope">
          <el-image
            style="width: 60px; height: 60px"
            :src="scope.row.image_url"
            fit="contain">
            <div slot="placeholder" class="load_image">
              <i class="el-icon-loading"></i>
            </div>
          </el-image>
        </template>
      </el-table-column>
      <el-table-column
        align="center"
        fixed="left"
        prop="username"
        label="微信号">
      </el-table-column>
      <el-table-column
        align="center"
        prop="sex"
        label="性别">
        <template slot-scope="scope">
          <span v-if="scope.row.sex == 1">男</span>
          <span v-else-if="scope.row.sex == 2">女</span>
        </template>
      </el-table-column>
      <el-table-column
        align="center"
        prop="city"
        label="城市">
      </el-table-column>
      <el-table-column
        align="center"
        label="积分">
        <template slot-scope="scope">
          <el-input v-if="cur_index == scope.row.id" v-model="scope.row.score" placeholder="积分"></el-input>
          <span v-else>{{ scope.row.score }}</span>
        </template>
      </el-table-column>
      <el-table-column
        align="center"
        label="经验">
        <template slot-scope="scope">
          <el-input v-if="cur_index == scope.row.id" v-model="scope.row.experience" placeholder="经验"></el-input>
          <span v-else>{{ scope.row.experience }}</span>
        </template>
      </el-table-column>
      <el-table-column
        align="center"
        label="管理员">
        <template slot-scope="scope">
          <div v-if="cur_index == scope.row.id">
            <el-switch v-model="scope.row.is_admin"></el-switch>
          </div>
          <div v-else>
            <el-button
              v-if="scope.row.is_admin"
              type="primary"
              icon="el-icon-check"
              size="mini"
              circle>
            </el-button>
            <el-button
              v-if="!scope.row.is_admin"
              icon="el-icon-close"
              size="mini"
              circle>
            </el-button>
          </div>
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
        search_val: '',
        cur_index: -1,
        last_score: 0,
        last_experience: 0,
        last_is_admin: false,
        table_data: [],
        cur_page: 1,
        page_size: 0,
        total: 0
      }
    },
    created () {
      this.getData();
      let self = this;
      document.onkeydown = function (e) {
        let key = window.event.keyCode;
        if (key == 13) {
          self.handleSearch();
        }
      };
    },
    methods: {
      getData (cur_page = 1, search_val = '') {
        let params = {
          cur_page: cur_page
        }
        if (search_val) {
          params.search_val = search_val;
        }
        this.$axios.get('/api/admin/user', {params: params})
          .then((res) => {
            this.table_data = res.data.data;
            this.page_size = res.data.page_size;
            this.total = res.data.total;
          })
          .catch((err) => {
            console.log(err);
          })
      },
      handleSearch () {
        this.getData(1, this.search_val);
      },
      handleSave (row) {
        let data = new FormData();
        data.append('id', row.id);
        data.append('score', row.score);
        data.append('experience', row.experience);
        data.append('is_admin', row.is_admin);
        this.$axios.put('/api/admin/user', data)
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
            data.score = this.last_score;
            data.experience = this.last_experience;
            data.is_admin = this.last_is_admin;
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
        this.last_score = row.score;
        this.last_experience = row.experience;
        this.last_is_admin = row.is_admin;
        this.cur_index = row.id;
      },
      handleDelete (row) {
        this.$confirm('此操作将永久删除该用户, 是否继续?', '提示', {
          cancelButtonText: '取消',
          confirmButtonText: '确定',
          type: 'warning',
          center: true
        }).then(() => {
          let data = new FormData();
          data.append('id', row.id);
          this.$axios.delete('/api/admin/user', {data: data})
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
            message: '已取消删除',
            showClose: true
          });
        });
      },
      currentChange (cur_page) {
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

  .load_image {
    font-size: 20px;
    line-height: 60px;
  }

  .footer {
    margin-top: 12px;
    margin-bottom: 12px;
    padding: 10px;
    text-align: center;
    background: #ffffff;
  }
</style>

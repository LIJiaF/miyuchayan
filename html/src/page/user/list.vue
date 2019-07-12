<template>
  <div class="main">
    <!--功能区-->
    <div class="banner">
      <el-row type="flex" align="middle">
        <el-col :md="6">
          <el-input
            placeholder="搜索微信号"
            prefix-icon="el-icon-search"
            v-model="search_val">
          </el-input>
        </el-col>
        <el-col :md="4">
          <el-button @click="handleSearch" size="medium" type="primary" style="margin-left: 10px;">搜索</el-button>
        </el-col>
        <el-col :md="3">
          <el-radio v-model="is_admin" label="1" border size="medium" @change="handleFilter">普通用户</el-radio>
        </el-col>
        <el-col :md="3">
          <el-radio v-model="is_admin" label="2" border size="medium" @change="handleFilter">管理员</el-radio>
        </el-col>
        <el-col :md="3">
          <el-radio v-model="is_admin" label="3" border size="medium" @change="handleFilter">全部</el-radio>
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
        min-width="140"
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
              @click="handleDialog(scope.row)"
              type="text">赠送
            </el-button>
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
    <!--隐藏-->
    <el-dialog title="优惠券列表" :visible.sync="dialogTableVisible" :modal-append-to-body='false' @close="dialogClose">
      <el-table
        :data="dialog_data"
        style="width: 100%">
        <el-table-column
          align="center"
          min-width="100"
          prop="name"
          label="优惠券类型">
        </el-table-column>
        <el-table-column
          align="center"
          prop="discount"
          label="折扣">
        </el-table-column>
        <el-table-column
          align="center"
          prop="score"
          label="积分">
        </el-table-column>
        <el-table-column
          align="center"
          prop="count"
          label="剩余数量">
        </el-table-column>
        <el-table-column
          min-width="250"
          prop="rule"
          label="使用规则">
        </el-table-column>
        <el-table-column
          align="center"
          label="状态">
          <template slot-scope="scope">
            <div>
              <el-button
                v-if="scope.row.state"
                type="primary"
                icon="el-icon-check"
                size="mini"
                circle>
              </el-button>
              <el-button
                v-if="!scope.row.state"
                icon="el-icon-close"
                size="mini"
                circle>
              </el-button>
            </div>
          </template>
        </el-table-column>
        <el-table-column
          fixed="right"
          min-width="50"
          label="操作">
          <template slot-scope="scope">
            <el-button
              @click="handleDiscountDialog(scope.row)"
              type="text">赠送
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-dialog>
  </div>
</template>

<script>
  export default {
    data () {
      return {
        search_val: '',
        is_admin: '1',
        cur_index: -1,
        cur_user: -1,
        last_score: 0,
        last_experience: 0,
        last_is_admin: false,
        table_data: [],
        cur_page: 1,
        page_size: 0,
        total: 0,
        dialogTableVisible: false,
        dialog_data: []
      }
    },
    created () {
      this.getData();
      this.getDialogData();
      let self = this;
      document.onkeydown = function (e) {
        let key = window.event.keyCode;
        if (key == 13) {
          self.handleSearch();
        }
      };
    },
    methods: {
      // 获取用户列表数据
      getData (cur_page = 1) {
        let params = {};
        params.cur_page = cur_page;
        params.search_val = this.search_val;
        params.is_admin = this.is_admin;
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
      // 获取优惠券列表数据
      getDialogData () {
        this.$axios.get('/api/admin/discount')
          .then((res) => {
            this.dialog_data = res.data.data;
          })
          .catch((err) => {
            console.log(err);
          })
      },
      // 用户列表赠送按钮
      handleDialog (row) {
        this.dialogTableVisible = true;
        this.cur_user = row.openid;
      },
      // 优惠券列表赠送按钮
      handleDiscountDialog (row) {
        let data = new FormData();
        data.append('discount_id', row.id);
        data.append('openid', this.cur_user);
        this.$axios.post('/api/admin/user/discount/rel', data)
          .then((res) => {
            if (!res.data.code) {
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
      dialogClose () {
        this.cur_user = -1;
      },
      handleSearch () {
        this.getData();
      },
      handleFilter () {
        this.getData();
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
          data.append('openid', row.openid);
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

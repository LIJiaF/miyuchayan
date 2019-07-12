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
          <el-radio v-model="end_time" label="1" border size="medium" @change="handleFilter">未过期</el-radio>
        </el-col>
        <el-col :md="3">
          <el-radio v-model="end_time" label="2" border size="medium" @change="handleFilter">已过期</el-radio>
        </el-col>
        <el-col :md="3">
          <el-radio v-model="end_time" label="3" border size="medium" @change="handleFilter">全部</el-radio>
        </el-col>
        <el-col :md="3">
          <el-radio v-model="use_state" label="1" border size="medium" @change="handleFilter">未使用</el-radio>
        </el-col>
        <el-col :md="3">
          <el-radio v-model="use_state" label="2" border size="medium" @change="handleFilter">已使用</el-radio>
        </el-col>
        <el-col :md="3">
          <el-radio v-model="use_state" label="3" border size="medium" @change="handleFilter">全部</el-radio>
        </el-col>
      </el-row>
    </div>
    <!--数据列表-->
    <el-table
      :data="table_data"
      style="width: 100%">
      <el-table-column type="expand">
        <template slot-scope="props">
          <el-table
            :data="props.row.discount_id"
            label-position="left"
            style="width: 100%">
            <el-table-column
              align="center"
              prop="type"
              min-width="100"
              label="优惠券类型">
            </el-table-column>
            <el-table-column
              align="center"
              prop="discount"
              label="折扣">
            </el-table-column>
            <el-table-column
              min-width="250"
              prop="rule"
              label="使用规则">
            </el-table-column>
            <el-table-column
              align="center"
              min-width="95"
              prop="end_time"
              label="截止日期">
            </el-table-column>
            <el-table-column
              align="center"
              fixed="right"
              label="状态">
              <template slot-scope="scope">
                <div v-if="cur_user == scope.row.user_id && cur_index == scope.row.id">
                  <el-switch v-model="scope.row.state"></el-switch>
                </div>
                <div v-else>
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
              min-width="95"
              label="操作">
              <template slot-scope="scope">
                <div v-if="cur_user == scope.row.user_id && cur_index == scope.row.id">
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
        </template>
      </el-table-column>
      <el-table-column
        prop="username"
        label="微信号">
      </el-table-column>
      <el-table-column
        align="center"
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
        prop="discount_count"
        align="center"
        label="优惠券数量">
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
        end_time: '1',
        use_state: '1',
        cur_user: -1,
        cur_index: -1,
        last_state: false,
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
      getData (cur_page = 1) {
        let params = {};
        params.cur_page = cur_page;
        params.search_val = this.search_val;
        params.end_time = this.end_time;
        params.use_state = this.use_state;
        this.$axios.get('/api/admin/user/discount/rel', {params: params})
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
        this.getData();
      },
      handleFilter () {
        this.getData();
      },
      handleSave (row) {
        let data = new FormData();
        data.append('id', row.id);
        data.append('state', row.state);
        this.$axios.put('/api/admin/user/discount/rel', data)
          .then((res) => {
            if (!res.data.code) {
              this.cur_index = -1;
              this.cur_user = -1;
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
        this.table_data.map((user) => {
          if (user.id == row.user_id) {
            user.discount_id.map((discount) => {
              if (discount.id == row.id) {
                discount.state = this.last_state;
              }
            });
          }
        });
        this.cur_user = -1;
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
        this.last_state = row.state;
        this.cur_user = row.user_id;
        this.cur_index = row.id;
      },
      handleDelete (row) {
        this.$confirm('此操作将永久删除该用户优惠券, 是否继续?', '提示', {
          cancelButtonText: '取消',
          confirmButtonText: '确定',
          type: 'warning',
          center: true
        }).then(() => {
          let data = new FormData();
          data.append('id', row.id);
          this.$axios.delete('/api/admin/user/discount/rel', {data: data})
            .then((res) => {
              if (!res.data.code) {
                this.table_data.map((user) => {
                  if (user.id == row.user_id) {
                    let index = user.discount_id.indexOf(row);
                    user.discount_id.splice(index, 1);
                  }
                });
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

  .footer {
    margin-top: 12px;
    margin-bottom: 12px;
    padding: 10px;
    text-align: center;
    background: #ffffff;
  }
</style>

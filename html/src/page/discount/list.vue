<template>
  <div class="main">
    <!--功能区-->
    <div class="banner">
      <router-link to="/discount/add">
        <el-button size="medium" type="primary">新增</el-button>
      </router-link>
    </div>
    <!--数据列表-->
    <el-table
      :data="table_data"
      style="width: 100%">
      <el-table-column
        align="center"
        min-width="100"
        label="优惠券类型">
        <template slot-scope="scope">
          <el-select
            v-if="cur_index == scope.row.id"
            prefix="scope.row.name"
            v-model="scope.row.type_id"
            @change="selectChange"
            placeholder="请选择优惠券类型">
            <el-option
              v-for="item in options"
              :key="item.id"
              :label="item.name"
              :value="item.id">
            </el-option>
          </el-select>
          <span v-else>{{ scope.row.name }}</span>
        </template>
      </el-table-column>
      <el-table-column
        align="center"
        label="折扣">
        <template slot-scope="scope">
          <el-input v-if="cur_index == scope.row.id" v-model="scope.row.discount" placeholder="折扣"></el-input>
          <span v-else>{{ scope.row.discount }}</span>
        </template>
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
        label="剩余数量">
        <template slot-scope="scope">
          <el-input v-if="cur_index == scope.row.id" v-model="scope.row.count" placeholder="数量"></el-input>
          <span v-else>{{ scope.row.count }}</span>
        </template>
      </el-table-column>
      <el-table-column
        min-width="250"
        prop="rule"
        label="使用规则">
        <template slot-scope="scope">
          <el-input v-if="cur_index == scope.row.id" v-model="scope.row.rule" placeholder="规则"></el-input>
          <span v-else>{{ scope.row.rule }}</span>
        </template>
      </el-table-column>
      <el-table-column
        align="center"
        label="状态">
        <template slot-scope="scope">
          <div v-if="cur_index == scope.row.id">
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
        last_type_id: '',
        last_discount: '',
        last_score: '',
        last_count: '',
        last_rule: '',
        last_state: false,
        options: [],
        table_data: [],
        cur_page: 1,
        page_size: 0,
        total: 0
      }
    },
    computed: {},
    created () {
      this.getData();
    },
    methods: {
      getData (cur_page = 1) {
        let params = {
          cur_page: cur_page
        }
        this.$axios.get('/api/admin/discount', {params: params})
          .then((res) => {
            this.table_data = res.data.data;
            this.page_size = res.data.page_size;
            this.total = res.data.total;
            this.options = res.data.options;
          })
          .catch((err) => {
            console.log(err);
          })
      },
      selectChange (value) {
        let option = this.options.filter((option) => {
          return option.id == value;
        });
        console.log(option);
        let self = this;
        this.table_data.map((data) => {
          if (data.id == self.cur_index) {
            data.name = option[0].name;
          }
        });
      },
      handleSave (row) {
        let data = new FormData();
        data.append('id', row.id);
        data.append('type_id', row.type_id);
        data.append('discount', row.discount);
        data.append('score', row.score);
        data.append('count', row.count);
        data.append('rule', row.rule);
        data.append('state', row.state);
        this.$axios.put('/api/admin/discount', data)
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
            data.type_id = this.last_type_id;
            data.discount = this.last_discount;
            data.score = this.last_score;
            data.count = this.last_count;
            data.rule = this.last_rule;
            data.state = this.last_state;
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
        this.last_type_id = row.type_id;
        this.last_discount = row.discount;
        this.last_score = row.score;
        this.last_count = row.count;
        this.last_rule = row.rule;
        this.last_state = row.state;
        this.cur_index = row.id;
      },
      handleDelete (row) {
        let self = this;
        this.$confirm('此操作将永久删除该优惠券, 是否继续?', '提示', {
          cancelButtonText: '取消',
          confirmButtonText: '确定',
          type: 'warning',
          center: true
        }).then(() => {
          let data = new FormData();
          data.append('id', row.id);
          this.$axios.delete('/api/admin/discount', {data: data})
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

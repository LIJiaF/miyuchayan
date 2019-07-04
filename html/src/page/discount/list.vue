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
          <el-select v-if="cur_index == scope.row.id" v-model="scope.row.type_id" placeholder="请选择优惠券类型">
            <el-option label="满减券" value="满减券"></el-option>
            <el-option label="折扣券" value="折扣券"></el-option>
            <el-option label="兑换券" value="兑换券"></el-option>
          </el-select>
          <span v-else>{{ scope.row.type_id }}</span>
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
        this.$axios.get('/api/admin/discount', {params: params})
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
        this.cur_index = -1;
        this.$message({
          message: '保存成功',
          type: 'success',
          showClose: true
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
      },
      handleEdit (row) {
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
          let index = self.table_data.indexOf(row);
          if (index != -1) {
            self.table_data.splice(index, 1);
          }
          this.$message({
            type: 'success',
            message: '删除成功!'
          });
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消删除'
          });
        });
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
</style>

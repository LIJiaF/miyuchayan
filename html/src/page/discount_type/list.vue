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
  </div>
</template>

<script>
  export default {
    data () {
      return {
        cur_index: -1,
        last_type: '',
        last_name: '',
        table_data: [{
          id: 1,
          type: 'exchange',
          name: '兑换券'
        }]
      }
    },
    methods: {
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
            data.type = this.last_type;
            data.name = this.last_name;
          }
        });
        this.cur_index = -1;
      },
      handleEdit (row) {
        this.last_type = row.type;
        this.last_name = row.name;
        this.cur_index = row.id;
      },
      handleDelete (row) {
        let self = this;
        this.$confirm('此操作将永久删除该优惠券类型, 是否继续?', '提示', {
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

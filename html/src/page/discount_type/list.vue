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
        prop="type"
        label="类型">
      </el-table-column>
      <el-table-column
        align="center"
        prop="name"
        label="名称">
      </el-table-column>
      <el-table-column
        fixed="right"
        min-width="95"
        label="操作">
        <template slot-scope="scope">
          <el-button @click="handleClick(scope.row)" type="text">修改</el-button>
          <el-button @click="handleClick(scope.row)" type="text">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
  export default {
    data () {
      return {
        table_data: [{
          type: 'exchange',
          name: '兑换券'
        }]
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

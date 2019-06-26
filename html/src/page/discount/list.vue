<template>
  <div class="main">
    <el-table
      :data="tableData"
      style="width: 100%">
      <el-table-column
        align="center"
        prop="type_id"
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
        width="250"
        prop="rule"
        label="使用规则">
      </el-table-column>
      <el-table-column
        align="center"
        label="状态">
        <template slot-scope="scope">
          <el-button
            v-if="scope.row.state == true"
            type="primary"
            icon="el-icon-check"
            size="mini"
            circle>
          </el-button>
          <el-button
            v-if="scope.row.state == false"
            icon="el-icon-close"
            size="mini"
            circle>
          </el-button>
        </template>
      </el-table-column>
      <el-table-column
        fixed="right"
        label="操作">
        <template slot-scope="scope">
          <el-button @click="handleClick(scope.row)" type="text" size="small">预览</el-button>
          <el-button @click="handleClick(scope.row)" type="text" size="small">修改</el-button>
          <el-button @click="handleClick(scope.row)" type="text" size="small">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
  export default {
    data () {
      return {
        tableData: [{
          type_id: '兑换券',
          discount: '奶茶',
          score: 20,
          count: 20,
          rule: '任意消费，可免费兑换一杯中杯奶茶',
          state: true
        }]
      }
    }
  }
</script>

<style scoped>
  .main {
    padding: 12px;
  }
</style>

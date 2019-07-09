<template>
  <div class="main">
    <div class="gather">
      <el-row :gutter="15">
        <el-col :span="8">
          <el-card class="box-card">
            <h1 class="total">粉丝总数：200</h1>
            <p class="detailed">男性：100</p>
            <p class="detailed">女性：100</p>
            <div class="report">
              ...
            </div>
          </el-card>
        </el-col>
        <el-col :span="8">
          <el-card class="box-card">
            <h1 class="total">优惠券总数：200</h1>
            <p class="detailed">已使用：100</p>
            <p class="detailed">未使用：100</p>
            <div class="report">
              ...
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script>
  export default {
    name: "main"
  }
</script>

<style scoped>
  .main {
    padding: 12px;
  }

  .total {
    font-size: 18px;
    font-weight: normal;
  }

  .detailed {
    display: inline-block;
    font-size: 14px;
    width: 48%;
    padding-top: 15px;
  }
</style>

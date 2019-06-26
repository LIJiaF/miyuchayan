<template>
  <div class="main">
    <el-table
      :data="tableData"
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
        fixed="left"
        label="微信号">
        <template slot-scope="scope">
          <span style="margin-left: 10px">{{ scope.row.username }}</span>
        </template>
      </el-table-column>
      <el-table-column
        align="center"
        prop="city"
        label="城市">
      </el-table-column>
      <el-table-column
        align="center"
        prop="score"
        label="积分">
      </el-table-column>
      <el-table-column
        align="center"
        prop="experience"
        label="经验">
      </el-table-column>
      <el-table-column
        align="center"
        label="管理员">
        <template slot-scope="scope">
          <el-button
            v-if="scope.row.is_admin == true"
            type="primary"
            icon="el-icon-check"
            size="mini"
            circle>
          </el-button>
          <el-button
            v-if="scope.row.is_admin == false"
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
          username: '李家富',
          image_url: 'http://thirdwx.qlogo.cn/mmopen/vi_32/Q0EBmjmic8Is2ezTGhysF7JcUjSjnNVOYrCVoOJ6hIBNziaQiaFN76OSIpa7OpdibS3Zp7yzwUUHibdqgVxRpIic6KPA/132',
          city: '广州',
          score: 20,
          experience: 20,
          is_admin: true
        }, {
          username: '李家富',
          image_url: 'http://thirdwx.qlogo.cn/mmopen/vi_32/Q0EBmjmic8Is2ezTGhysF7JcUjSjnNVOYrCVoOJ6hIBNziaQiaFN76OSIpa7OpdibS3Zp7yzwUUHibdqgVxRpIic6KPA/132',
          city: '广州',
          score: 20,
          experience: 20,
          is_admin: false
        }]
      }
    }
  }
</script>

<style scoped>
  .main {
    padding: 12px;
  }

  .load_image {
    font-size: 20px;
    line-height: 60px;
  }
</style>

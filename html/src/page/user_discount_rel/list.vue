<template>
  <div class="main">
    <el-table
      :data="tableData"
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
              prop="end_time"
              label="截止日期">
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
              min-width="95"
              label="操作">
              <template slot-scope="scope">
                <el-button @click="handleClick(scope.row)" type="text">修改</el-button>
                <el-button @click="handleClick(scope.row)" type="text">删除</el-button>
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
    </el-table>
  </div>
</template>

<script>
  export default {
    data () {
      return {
        tableData: [{
          image_url: 'http://thirdwx.qlogo.cn/mmopen/vi_32/Q0EBmjmic8Is2ezTGhysF7JcUjSjnNVOYrCVoOJ6hIBNziaQiaFN76OSIpa7OpdibS3Zp7yzwUUHibdqgVxRpIic6KPA/132',
          username: '李家富',
          discount_id: [
            {
              type: '兑换券',
              discount: '奶茶',
              rule: '任意消费，可免费兑换一杯中杯奶茶',
              end_time: '2019-06-27',
              'use_time': '2019-06-27',
              state: false
            },
            {
              type: '兑换券',
              discount: '奶茶',
              rule: '任意消费，可免费兑换一杯中杯奶茶',
              end_time: '2019-06-27',
              'use_time': '2019-06-27',
              state: true
            }
          ]
        }, {
          image_url: 'http://thirdwx.qlogo.cn/mmopen/vi_32/Q0EBmjmic8Is2ezTGhysF7JcUjSjnNVOYrCVoOJ6hIBNziaQiaFN76OSIpa7OpdibS3Zp7yzwUUHibdqgVxRpIic6KPA/132',
          username: '李家富',
          discount_id: [
            {
              type: '兑换券',
              discount: '奶茶',
              rule: '任意消费，可免费兑换一杯中杯奶茶',
              end_time: '2019-06-27',
              'use_time': '2019-06-27',
              state: false
            },
            {
              type: '兑换券',
              discount: '奶茶',
              rule: '任意消费，可免费兑换一杯中杯奶茶',
              end_time: '2019-06-27',
              'use_time': '2019-06-27',
              state: true
            }
          ]
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

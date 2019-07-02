<template>
  <div class="main">
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
        cur_user: -1,
        cur_index: -1,
        last_state: false,
        table_data: [{
          id: 1,
          image_url: 'http://thirdwx.qlogo.cn/mmopen/vi_32/Q0EBmjmic8Is2ezTGhysF7JcUjSjnNVOYrCVoOJ6hIBNziaQiaFN76OSIpa7OpdibS3Zp7yzwUUHibdqgVxRpIic6KPA/132',
          username: '李家富',
          discount_id: [
            {
              id: 1,
              user_id: 1,
              type: '兑换券',
              discount: '奶茶',
              rule: '任意消费，可免费兑换一杯中杯奶茶',
              end_time: '2019-06-27',
              'use_time': '2019-06-27',
              state: false
            },
            {
              id: 2,
              user_id: 1,
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
    },
    methods: {
      handleSave (row) {
        this.cur_index = -1;
        this.cur_user = -1;
        this.$message({
          message: '保存成功',
          type: 'success',
          showClose: true
        });
      },
      handleCancel (row) {
        this.table_data.map((user) => {
          if (user.id == row.user_id) {
            user.discount_id.map((discount) => {
              if (discount.id = row.id) {
                discount.state = row.state;
              }
            });
          }
        });
        this.cur_index = -1;
        this.cur_user = -1;
      },
      handleEdit (row) {
        this.last_state = row.state;
        this.cur_user = row.user_id;
        this.cur_index = row.id;
      },
      handleDelete (row) {
        let self = this;
        this.$confirm('此操作将永久删除该用户优惠券, 是否继续?', '提示', {
          cancelButtonText: '取消',
          confirmButtonText: '确定',
          type: 'warning',
          center: true
        }).then(() => {
          self.table_data.map((user) => {
            if (user.id == row.user_id) {
              let index = user.discount_id.indexOf(row);
              if (index != -1) {
                user.discount_id.splice(index, 1);
                return;
              }
            }
          });
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
</style>

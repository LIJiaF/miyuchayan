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
                <div v-if="cur_user == scope.row.id && cur_index == scope.row.id">
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
        tableData: [{
          id: 1,
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
        this.table_data.discount_id.map((data) => {
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
        this.cur_user = row.id;
        this.cur_index = row.discount_id.id;
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
</style>

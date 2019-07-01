<template>
  <div class="main">
    <!--功能区-->
    <div class="banner">
      <el-row type="flex" :gutter="10" align="middle">
        <el-col :span="8">
          <el-input
            placeholder="搜索微信号"
            prefix-icon="el-icon-search"
            v-model="search_val">
          </el-input>
        </el-col>
        <el-col :span="4">
          <el-button @click="handleSearch" size="medium" type="primary">搜索</el-button>
        </el-col>
      </el-row>
    </div>
    <!--数据列表-->
    <el-table
      :data="table_data"
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
        align="center"
        fixed="left"
        prop="username"
        label="微信号">
      </el-table-column>
      <el-table-column
        align="center"
        prop="city"
        label="城市">
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
        label="经验">
        <template slot-scope="scope">
          <el-input v-if="cur_index == scope.row.id" v-model="scope.row.experience" placeholder="经验"></el-input>
          <span v-else>{{ scope.row.experience }}</span>
        </template>
      </el-table-column>
      <el-table-column
        align="center"
        label="管理员">
        <template slot-scope="scope">
          <div v-if="cur_index == scope.row.id">
            <el-switch v-model="scope.row.is_admin"></el-switch>
          </div>
          <div v-else>
            <el-button
              v-if="scope.row.is_admin"
              type="primary"
              icon="el-icon-check"
              size="mini"
              circle>
            </el-button>
            <el-button
              v-if="!scope.row.is_admin"
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
        search_val: '',
        cur_index: -1,
        last_score: 0,
        last_experience: 0,
        last_is_admin: false,
        table_data: [{
          id: 1,
          username: '李家富',
          image_url: 'http://thirdwx.qlogo.cn/mmopen/vi_32/Q0EBmjmic8Is2ezTGhysF7JcUjSjnNVOYrCVoOJ6hIBNziaQiaFN76OSIpa7OpdibS3Zp7yzwUUHibdqgVxRpIic6KPA/132',
          city: '广州',
          score: 20,
          experience: 20,
          is_admin: true
        }, {
          id: 2,
          username: '李家富',
          image_url: 'http://thirdwx.qlogo.cn/mmopen/vi_32/Q0EBmjmic8Is2ezTGhysF7JcUjSjnNVOYrCVoOJ6hIBNziaQiaFN76OSIpa7OpdibS3Zp7yzwUUHibdqgVxRpIic6KPA/132',
          city: '广州',
          score: 20,
          experience: 20,
          is_admin: false
        }]
      }
    },
    methods: {
      handleSearch () {
        console.log(this.search_val);
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
            data.score = this.last_score;
            data.experience = this.last_experience;
            data.is_admin = this.last_is_admin;
          }
        });
        this.cur_index = -1;
      },
      handleEdit (row) {
        this.last_score = row.score;
        this.last_experience = row.experience;
        this.last_is_admin = row.is_admin;
        this.cur_index = row.id;
      },
      handleDelete (row) {
        let self = this;
        this.$confirm('此操作将永久删除该用户, 是否继续?', '提示', {
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

  .load_image {
    font-size: 20px;
    line-height: 60px;
  }
</style>

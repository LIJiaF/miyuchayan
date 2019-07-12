<template>
  <div class="main">
    <el-form ref="form" label-width="82px">
      <el-form-item label="用户名">
        <el-input v-model="username" style="width:216px;" label="折扣"></el-input>
      </el-form-item>
      <el-form-item label="密 码">
        <el-input type="password" v-model="password" style="width:216px;" label="折扣"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="editPassword">修改</el-button>
        <router-link to="/main">
          <el-button>返回</el-button>
        </router-link>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
  export default {
    name: "edit_password",
    data () {
      return {
        username: '',
        password: ''
      }
    },
    created () {
      this.username = sessionStorage.getItem('username');
    },
    methods: {
      editPassword () {
        let data = new FormData;
        data.append('username', this.username);
        data.append('password', this.password);
        this.$axios.post('/api/admin/edit/password', data)
          .then((res) => {
            if (!res.data.code) {
              this.$message({
                message: res.data.msg,
                type: 'success',
                showClose: true
              });
              this.$router.push('/');
            } else {
              this.$message({
                message: res.data.msg,
                type: 'error',
                showClose: true
              });
            }
          })
          .catch((err) => {
            console.log(err);
          })
      }
    }
  }
</script>

<style scoped>
  .main {
    margin: 12px auto;
    padding: 40px 50px 10px;
    width: 350px;
    border-radius: 10px;
    background: #ffffff;
  }
</style>

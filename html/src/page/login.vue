<template>
  <div class="main">
    <!--表单-->
    <div class="form">
      <h1 class="title">密语茶言后台管理系统</h1>
      <p>
        <el-input
          placeholder="账号"
          v-model="username">
          <i slot="prefix" class="el-input__icon el-icon-user-solid"></i>
        </el-input>
      </p>
      <p>
        <el-input
          placeholder="密码"
          type="password"
          v-model="password">
          <i slot="prefix" class="el-input__icon el-icon-s-goods"></i>
        </el-input>
      </p>
      <p class="btn">
        <el-button type="primary" round @click="handleLogin">登 陆</el-button>
      </p>
    </div>
  </div>
</template>

<script>
  export default {
    data () {
      return {
        username: '',
        password: ''
      }
    },
    created () {
      // 删除sessionStorage
      sessionStorage.removeItem('username');
      // 删除cookie
      this.delCookie('username');

      let _this = this;
      document.onkeydown = function (e) {
        let key = window.event.keyCode;
        if (key == 13) {
          _this.handleLogin();
        }
      };
    },
    methods: {
      getCookie (name) {
        let arr, reg = new RegExp("(^| )" + name + "=([^;]*)(;|$)");
        if (arr = document.cookie.match(reg))
          return unescape(arr[2]);
        else
          return null;
      },
      delCookie (name) {
        let exp = new Date();
        exp.setTime(exp.getTime() - 1);
        let cval = this.getCookie(name);
        if (cval != null)
          document.cookie = name + "=" + cval + ";expires=" + exp.toGMTString();
      },
      handleLogin () {
        if (!this.username || !this.password) {
          this.$message({
            message: '账号或密码不能为空！',
            type: 'error',
            showClose: true
          });
          return;
        }

        let data = new FormData();
        data.append('username', this.username);
        data.append('password', this.password);
        this.$axios.post('/api/admin/login', data)
          .then((res) => {
            if (!res.data.code) {
              sessionStorage.setItem('username', this.username);
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
  .form {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 350px;
    padding: 40px;
    box-shadow: 0 0 2px #6495ED inset;
    border-radius: 10px;
    background: #ffffff;
  }

  .title {
    padding-bottom: 35px;
    font-weight: normal;
    text-align: center;
    color: #6495ED;
  }

  .form p {
    padding: 10px 50px;
  }

  .btn {
    margin-top: 15px;
    margin-bottom: -15px;
    text-align: center;
  }

  .btn button {
    width: 150px;
    letter-spacing: 8px;
  }
</style>

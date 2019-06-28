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
          v-model="password">
          <i slot="prefix" class="el-input__icon el-icon-s-goods"></i>
        </el-input>
      </p>
      <p class="btn">
        <el-button type="primary" round @click="onSubmit">登 陆</el-button>
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
    methods: {
      onSubmit () {
        alert('11');
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

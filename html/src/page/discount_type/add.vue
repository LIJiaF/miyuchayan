<template>
  <div class="main">
    <el-form ref="form" :model="data" label-width="82px">
      <el-form-item label="类型">
        <el-input v-model="data.type" placeholder="类型"></el-input>
      </el-form-item>
      <el-form-item label="名称">
        <el-input v-model="data.name" placeholder="名称"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="handleSave">添加</el-button>
        <router-link to="/discount/type">
          <el-button>返回</el-button>
        </router-link>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
  export default {
    name: "add",
    data () {
      return {
        data: {
          type: '',
          name: ''
        }
      }
    },
    methods: {
      handleSave () {
        if (!this.data.type) {
          this.$message({
            message: '类型不能为空！',
            type: 'error',
            showClose: true
          });
          return;
        }
        if (!this.data.name) {
          this.$message({
            message: '名称不能为空！',
            type: 'error',
            showClose: true
          });
          return;
        }
        let data = new FormData();
        data.append('type', this.data.type);
        data.append('name', this.data.name);
        this.$axios.post('/api/admin/discount/type', data)
          .then((res) => {
            if (!res.data.code) {
              this.$message({
                message: res.data.msg,
                type: 'success',
                showClose: true
              });
              this.$router.push('/discount/type');
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
    padding: 30px 50px 10px;
    width: 500px;
    border-radius: 10px;
    background: #ffffff;
  }
</style>

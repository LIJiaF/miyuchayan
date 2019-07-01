<template>
  <div class="main">
    <el-form ref="form" :model="discount_type" label-width="82px">
      <el-form-item label="类型">
        <el-input v-model="discount_type.type" placeholder="类型"></el-input>
      </el-form-item>
      <el-form-item label="名称">
        <el-input v-model="discount_type.name" placeholder="名称"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="handleSave">保存</el-button>
        <router-link to="/discount/type">
          <el-button>取消</el-button>
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
        discount_type: {
          type: '',
          name: ''
        }
      }
    },
    methods: {
      handleSave () {
        console.log('handleSave');
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

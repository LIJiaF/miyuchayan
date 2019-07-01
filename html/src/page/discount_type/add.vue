<template>
  <div class="main">
    <el-form ref="form" :model="discount" label-width="82px">
      <el-form-item label="优惠券类型">
        <el-select v-model="discount.type" placeholder="请选择优惠券类型">
          <el-option label="满减券" value="money"></el-option>
          <el-option label="折扣券" value="discount"></el-option>
          <el-option label="兑换券" value="exchange"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="折扣">
        <el-input-number v-model="discount.discount" :min="1" label="折扣"></el-input-number>
      </el-form-item>
      <el-form-item label="积分">
        <el-input-number v-model="discount.score" :min="1" label="积分"></el-input-number>
      </el-form-item>
      <el-form-item label="是否启用">
        <el-switch v-model="discount.state"></el-switch>
      </el-form-item>
      <el-form-item label="使用规则">
        <el-input type="textarea" v-model="discount.rule"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="handleSave">保存</el-button>
        <el-button>取消</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
  export default {
    name: "add",
    data () {
      return {
        discount: {
          type: '',
          discount: '',
          score: '',
          state: false,
          rule: ''
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

<template>
  <div class="main">
    <el-form ref="form" :model="data" label-width="82px">
      <el-form-item label="优惠券类型">
        <el-select v-model="data.type_id" placeholder="请选择优惠券类型">
          <el-option
            v-for="item in options"
            :key="item.id"
            :label="item.name"
            :value="item.id">
          </el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="折扣">
        <el-input v-model="data.discount" style="width:216px;" label="折扣"></el-input>
      </el-form-item>
      <el-form-item label="积分">
        <el-input-number v-model="data.score" :min="1" label="积分"></el-input-number>
      </el-form-item>
      <el-form-item label="是否启用">
        <el-switch v-model="data.state"></el-switch>
      </el-form-item>
      <el-form-item label="使用规则">
        <el-input type="textarea" v-model="data.rule"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="handleSave">添加</el-button>
        <router-link to="/discount">
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
        options: [],
        data: {
          type_id: '',
          discount: '',
          score: '',
          state: false,
          rule: ''
        }
      }
    },
    created () {
      this.getOptionsData();
    },
    methods: {
      getOptionsData () {
        this.$axios.get('/api/admin/discount/type', {params: {cur_page: 0}})
          .then((res) => {
            this.options = res.data;
          })
          .catch((err) => {
            console.log(err);
          })
      },
      handleSave () {
        if (!this.data.type_id) {
          this.$message({
            message: '优惠券类型不能为空！',
            type: 'error',
            showClose: true
          });
          return;
        }
        let data = new FormData();
        data.append('type_id', this.data.type_id);
        data.append('discount', this.data.discount);
        data.append('score', this.data.score);
        data.append('state', this.data.state);
        data.append('rule', this.data.rule);
        this.$axios.post('/api/admin/discount', data)
          .then((res) => {
            if (!res.data.code) {
              this.$message({
                message: res.data.msg,
                type: 'success',
                showClose: true
              });
              this.$router.push('/discount');
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

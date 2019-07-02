<template>
  <div id="app">
    <router-view/>
  </div>
</template>

<script>
  export default {
    name: 'App'
  }
</script>

<style>
  * {
    margin: 0;
    padding: 0;
    outline: none;
    font-family: Arial;
    list-style: none;
    text-decoration: none;
  }

  body {
    background: aliceblue;
  }

  /*Element 样式*/
  .el-menu {
    border-right: none;
  }

  .el-popover {
    min-width: 80px;
  }
</style>

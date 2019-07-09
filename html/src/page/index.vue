<template>
  <div class="main">
    <!--头部-->
    <div class="header">
      <h1 class="title">后台管理系统</h1>
      <ul class="menu">
        <router-link to="/">
          <li class="active">首页</li>
        </router-link>
      </ul>
      <p class="info">
        用户名：
        <el-popover
          placement="bottom"
          transition="fade-in-linear"
          trigger="hover">
          <ul class="popover" style="text-align: center">
            <router-link to="/edit/password">
              <li>修改密码</li>
            </router-link>
            <router-link to="/login">
              <li>退出</li>
            </router-link>
          </ul>
          <span class="user" slot="reference">admin</span>
        </el-popover>
      </p>
    </div>
    <div>
      <!--侧边栏-->
      <div class="aside">
        <el-menu
          default-active="1"
          class="el-menu-vertical-demo">
          <el-submenu index="1">
            <template slot="title">
              <i class="el-icon-user"></i>
              <span>用户管理</span>
            </template>
            <router-link to="/user">
              <el-menu-item index="1-1">用户列表</el-menu-item>
            </router-link>
          </el-submenu>
          <el-submenu index="2">
            <template slot="title">
              <i class="el-icon-postcard"></i>
              <span>优惠券管理</span>
            </template>
            <router-link to="/discount">
              <el-menu-item index="2-1">优惠券列表</el-menu-item>
            </router-link>
            <router-link to="/discount/type">
              <el-menu-item index="2-2">优惠券类型</el-menu-item>
            </router-link>
          </el-submenu>
          <el-submenu index="3">
            <template slot="title">
              <i class="el-icon-star-off"></i>
              <span>用户优惠券管理</span>
            </template>
            <router-link to="/user/discount/rel">
              <el-menu-item index="3-1">用户优惠券列表</el-menu-item>
            </router-link>
          </el-submenu>
        </el-menu>
      </div>
      <!--内容-->
      <div class="content">
        <router-view/>
      </div>
    </div>
  </div>
</template>

<style scoped>
  body {
    background: aliceblue;
  }

  .header {
    min-width: 525px;
    background: #6495ED;
    overflow: hidden;
  }

  .popover {
    text-align: center;
  }

  .popover li {
    padding: 10px 0;
  }

  .title {
    float: left;
    width: 250px;
    padding: 15px;
    font-size: 28px;
    text-align: center;
    color: #ffffff;
    box-sizing: border-box;
  }

  .menu {
    float: left;
    overflow: hidden;
  }

  .menu li {
    float: left;
    color: #ffffff;
    padding: 23px 20px;
  }

  .menu li.active {
    background: #673ab7;
  }

  .info {
    float: right;
    color: #ffffff;
  }

  .info span {
    height: 67px;
    line-height: 67px;
    padding-right: 15px;
  }

  .info a {
    color: #ffffff;
    text-decoration: none;
  }

  .info a:hover {
    color: #673ab7;
  }

  .aside {
    position: fixed;
    top: 67px;
    bottom: 0;
    width: 250px;
    background: #ffffff;
  }

  .content {
    position: fixed;
    top: 67px;
    left: 250px;
    right: 0;
    bottom: 0;
    overflow: auto;
  }
</style>

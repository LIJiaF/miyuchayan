webpackJsonp([0],{KhGW:function(e,s){},Ntyz:function(e,s,t){"use strict";Object.defineProperty(s,"__esModule",{value:!0});var a={data:function(){return{username:"",password:""}},created:function(){var e=this;document.onkeydown=function(s){13==window.event.keyCode&&e.handleLogin()}},methods:{handleLogin:function(){var e=this;if(this.username&&this.password){var s=new FormData;s.append("username",this.username),s.append("password",this.password),this.$axios.post("/api/admin/login",s).then(function(s){s.data.code?e.$message({message:s.data.msg,type:"error",showClose:!0}):(sessionStorage.setItem("username",e.username),e.$router.push("/"))}).catch(function(e){console.log(e)})}else this.$message({message:"账号或密码不能为空！",type:"error",showClose:!0})}}},n={render:function(){var e=this,s=e.$createElement,t=e._self._c||s;return t("div",{staticClass:"main"},[t("div",{staticClass:"form"},[t("h1",{staticClass:"title"},[e._v("密语茶言后台管理系统")]),e._v(" "),t("p",[t("el-input",{attrs:{placeholder:"账号"},model:{value:e.username,callback:function(s){e.username=s},expression:"username"}},[t("i",{staticClass:"el-input__icon el-icon-user-solid",attrs:{slot:"prefix"},slot:"prefix"})])],1),e._v(" "),t("p",[t("el-input",{attrs:{placeholder:"密码",type:"password"},model:{value:e.password,callback:function(s){e.password=s},expression:"password"}},[t("i",{staticClass:"el-input__icon el-icon-s-goods",attrs:{slot:"prefix"},slot:"prefix"})])],1),e._v(" "),t("p",{staticClass:"btn"},[t("el-button",{attrs:{type:"primary",round:""},on:{click:e.handleLogin}},[e._v("登 陆")])],1)])])},staticRenderFns:[]};var o=t("VU/8")(a,n,!1,function(e){t("KhGW")},"data-v-e61b4738",null);s.default=o.exports}});
//# sourceMappingURL=0.956931386f514090433e.js.map
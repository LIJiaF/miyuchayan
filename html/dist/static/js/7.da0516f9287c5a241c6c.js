webpackJsonp([7],{"5erv":function(e,t,a){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var n={data:function(){return{search_val:"",cur_index:-1,last_score:0,last_experience:0,last_is_admin:!1,table_data:[],cur_page:1,page_size:0,total:0}},created:function(){this.getData();var e=this;document.onkeydown=function(t){13==window.event.keyCode&&e.handleSearch()}},methods:{getData:function(){var e=this,t=arguments.length>0&&void 0!==arguments[0]?arguments[0]:1,a=arguments.length>1&&void 0!==arguments[1]?arguments[1]:"",n={cur_page:t};a&&(n.search_val=a),this.$axios.get("/api/admin/user",{params:n}).then(function(t){e.table_data=t.data.data,e.page_size=t.data.page_size,e.total=t.data.total}).catch(function(e){console.log(e)})},handleSearch:function(){this.getData(1,this.search_val)},handleSave:function(e){var t=this,a=new FormData;a.append("id",e.id),a.append("score",e.score),a.append("experience",e.experience),a.append("is_admin",e.is_admin),this.$axios.put("/api/admin/user",a).then(function(e){e.data.code?t.$message({message:e.data.msg,type:"error",showClose:!0}):(t.cur_index=-1,t.$message({message:e.data.msg,type:"success",showClose:!0}))}).catch(function(e){console.log(e)})},handleCancel:function(e){var t=this;this.table_data.map(function(a){a.id==e.id&&(a.score=t.last_score,a.experience=t.last_experience,a.is_admin=t.last_is_admin)}),this.cur_index=-1,this.$message({type:"info",message:"已取消",showClose:!0})},handleEdit:function(e){-1==this.cur_index?(this.last_score=e.score,this.last_experience=e.experience,this.last_is_admin=e.is_admin,this.cur_index=e.id):this.$message({message:"请保存或取消！",type:"warning",showClose:!0})},handleDelete:function(e){var t=this;this.$confirm("此操作将永久删除该用户, 是否继续?","提示",{cancelButtonText:"取消",confirmButtonText:"确定",type:"warning",center:!0}).then(function(){var a=new FormData;a.append("id",e.id),t.$axios.delete("/api/admin/user",{data:a}).then(function(e){e.data.code?t.$message({message:e.data.msg,type:"error",showClose:!0}):(t.cur_page>1&&t.table_data.length<=(t.cur_page-1)*t.page_size+1&&(t.cur_page=t.cur_page-1),t.getData(t.cur_page),t.$message({type:"success",message:e.data.msg,showClose:!0}))}).catch(function(e){console.log(e)})}).catch(function(){t.$message({type:"info",message:"已取消删除",showClose:!0})})},currentChange:function(e){this.getData(e)}}},s={render:function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",{staticClass:"main"},[a("div",{staticClass:"banner"},[a("el-row",{attrs:{type:"flex",gutter:10,align:"middle"}},[a("el-col",{attrs:{span:8}},[a("el-input",{attrs:{placeholder:"搜索微信号","prefix-icon":"el-icon-search"},model:{value:e.search_val,callback:function(t){e.search_val=t},expression:"search_val"}})],1),e._v(" "),a("el-col",{attrs:{span:4}},[a("el-button",{attrs:{size:"medium",type:"primary"},on:{click:e.handleSearch}},[e._v("搜索")])],1)],1)],1),e._v(" "),a("el-table",{staticStyle:{width:"100%"},attrs:{data:e.table_data}},[a("el-table-column",{attrs:{align:"center",fixed:"left",label:"头像"},scopedSlots:e._u([{key:"default",fn:function(e){return[a("el-image",{staticStyle:{width:"60px",height:"60px"},attrs:{src:e.row.image_url,fit:"contain"}},[a("div",{staticClass:"load_image",attrs:{slot:"placeholder"},slot:"placeholder"},[a("i",{staticClass:"el-icon-loading"})])])]}}])}),e._v(" "),a("el-table-column",{attrs:{align:"center",fixed:"left",prop:"username",label:"微信号"}}),e._v(" "),a("el-table-column",{attrs:{align:"center",prop:"sex",label:"性别"},scopedSlots:e._u([{key:"default",fn:function(t){return[1==t.row.sex?a("span",[e._v("男")]):2==t.row.sex?a("span",[e._v("女")]):e._e()]}}])}),e._v(" "),a("el-table-column",{attrs:{align:"center",prop:"city",label:"城市"}}),e._v(" "),a("el-table-column",{attrs:{align:"center",label:"积分"},scopedSlots:e._u([{key:"default",fn:function(t){return[e.cur_index==t.row.id?a("el-input",{attrs:{placeholder:"积分"},model:{value:t.row.score,callback:function(a){e.$set(t.row,"score",a)},expression:"scope.row.score"}}):a("span",[e._v(e._s(t.row.score))])]}}])}),e._v(" "),a("el-table-column",{attrs:{align:"center",label:"经验"},scopedSlots:e._u([{key:"default",fn:function(t){return[e.cur_index==t.row.id?a("el-input",{attrs:{placeholder:"经验"},model:{value:t.row.experience,callback:function(a){e.$set(t.row,"experience",a)},expression:"scope.row.experience"}}):a("span",[e._v(e._s(t.row.experience))])]}}])}),e._v(" "),a("el-table-column",{attrs:{align:"center",label:"管理员"},scopedSlots:e._u([{key:"default",fn:function(t){return[e.cur_index==t.row.id?a("div",[a("el-switch",{model:{value:t.row.is_admin,callback:function(a){e.$set(t.row,"is_admin",a)},expression:"scope.row.is_admin"}})],1):a("div",[t.row.is_admin?a("el-button",{attrs:{type:"primary",icon:"el-icon-check",size:"mini",circle:""}}):e._e(),e._v(" "),t.row.is_admin?e._e():a("el-button",{attrs:{icon:"el-icon-close",size:"mini",circle:""}})],1)]}}])}),e._v(" "),a("el-table-column",{attrs:{fixed:"right","min-width":"95",label:"操作"},scopedSlots:e._u([{key:"default",fn:function(t){return[e.cur_index==t.row.id?a("div",[a("el-button",{attrs:{type:"text",size:"small"},on:{click:function(a){return e.handleSave(t.row)}}},[e._v("保存\n          ")]),e._v(" "),a("el-button",{attrs:{type:"text",size:"small"},on:{click:function(a){return e.handleCancel(t.row)}}},[e._v("取消\n          ")])],1):a("div",[a("el-button",{attrs:{type:"text"},on:{click:function(a){return e.handleEdit(t.row)}}},[e._v("修改\n          ")]),e._v(" "),a("el-button",{attrs:{type:"text"},on:{click:function(a){return e.handleDelete(t.row)}}},[e._v("删除\n          ")])],1)]}}])})],1),e._v(" "),a("div",{staticClass:"footer"},[a("el-pagination",{attrs:{background:"","page-size":e.page_size,layout:"prev, pager, next",total:e.total},on:{"current-change":e.currentChange}})],1)],1)},staticRenderFns:[]};var i=a("VU/8")(n,s,!1,function(e){a("JW4Y")},"data-v-074aad88",null);t.default=i.exports},JW4Y:function(e,t){}});
//# sourceMappingURL=7.da0516f9287c5a241c6c.js.map
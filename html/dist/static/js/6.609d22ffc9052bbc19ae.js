webpackJsonp([6],{mvyv:function(t,e){},sV29:function(t,e,a){"use strict";Object.defineProperty(e,"__esModule",{value:!0});var n={data:function(){return{cur_index:-1,last_type_id:"",last_discount:"",last_score:"",last_count:"",last_rule:"",last_state:!1,options:[],table_data:[],cur_page:1,page_size:0,total:0}},computed:{},created:function(){this.getData()},methods:{getData:function(){var t=this,e={cur_page:arguments.length>0&&void 0!==arguments[0]?arguments[0]:1};this.$axios.get("/api/admin/discount",{params:e}).then(function(e){t.table_data=e.data.data,t.page_size=e.data.page_size,t.total=e.data.total,t.options=e.data.options}).catch(function(t){console.log(t)})},selectChange:function(t){var e=this.options.filter(function(e){return e.id==t}),a=this;this.table_data.map(function(t){t.id==a.cur_index&&(t.name=e[0].name)})},handleSave:function(t){var e=this,a=new FormData;a.append("id",t.id),a.append("type_id",t.type_id),a.append("discount",t.discount),a.append("score",t.score),a.append("count",t.count),a.append("rule",t.rule),a.append("state",t.state),this.$axios.put("/api/admin/discount",a).then(function(t){t.data.code?e.$message({message:t.data.msg,type:"error",showClose:!0}):(e.cur_index=-1,e.$message({message:t.data.msg,type:"success",showClose:!0}))}).catch(function(t){console.log(t)})},handleCancel:function(t){var e=this;this.table_data.map(function(a){a.id==t.id&&(a.type_id=e.last_type_id,a.discount=e.last_discount,a.score=e.last_score,a.count=e.last_count,a.rule=e.last_rule,a.state=e.last_state)}),this.cur_index=-1,this.$message({type:"info",message:"已取消",showClose:!0})},handleEdit:function(t){-1==this.cur_index?(this.last_type_id=t.type_id,this.last_discount=t.discount,this.last_score=t.score,this.last_count=t.count,this.last_rule=t.rule,this.last_state=t.state,this.cur_index=t.id):this.$message({message:"请保存或取消！",type:"warning",showClose:!0})},handleDelete:function(t){var e=this;this.$confirm("此操作将永久删除该优惠券, 是否继续?","提示",{cancelButtonText:"取消",confirmButtonText:"确定",type:"warning",center:!0}).then(function(){var a=new FormData;a.append("id",t.id),e.$axios.delete("/api/admin/discount",{data:a}).then(function(t){t.data.code?e.$message({message:t.data.msg,type:"error",showClose:!0}):(e.cur_page>1&&e.table_data.length<=(e.cur_page-1)*e.page_size+1&&(e.cur_page=e.cur_page-1),e.getData(e.cur_page),e.$message({type:"success",message:t.data.msg,showClose:!0}))}).catch(function(t){console.log(t)})}).catch(function(){e.$message({type:"info",message:"已取消删除",showClose:!0})})},currentChange:function(t){this.cur_page=t,this.getData(t)}}},s={render:function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",{staticClass:"main"},[a("div",{staticClass:"banner"},[a("router-link",{attrs:{to:"/discount/add"}},[a("el-button",{attrs:{size:"medium",type:"primary"}},[t._v("新增")])],1)],1),t._v(" "),a("el-table",{staticStyle:{width:"100%"},attrs:{data:t.table_data}},[a("el-table-column",{attrs:{align:"center","min-width":"100",label:"优惠券类型"},scopedSlots:t._u([{key:"default",fn:function(e){return[t.cur_index==e.row.id?a("el-select",{attrs:{prefix:"scope.row.name",placeholder:"请选择优惠券类型"},on:{change:t.selectChange},model:{value:e.row.type_id,callback:function(a){t.$set(e.row,"type_id",a)},expression:"scope.row.type_id"}},t._l(t.options,function(t){return a("el-option",{key:t.id,attrs:{label:t.name,value:t.id}})}),1):a("span",[t._v(t._s(e.row.name))])]}}])}),t._v(" "),a("el-table-column",{attrs:{align:"center",label:"折扣"},scopedSlots:t._u([{key:"default",fn:function(e){return[t.cur_index==e.row.id?a("el-input",{attrs:{placeholder:"折扣"},model:{value:e.row.discount,callback:function(a){t.$set(e.row,"discount",a)},expression:"scope.row.discount"}}):a("span",[t._v(t._s(e.row.discount))])]}}])}),t._v(" "),a("el-table-column",{attrs:{align:"center",label:"积分"},scopedSlots:t._u([{key:"default",fn:function(e){return[t.cur_index==e.row.id?a("el-input",{attrs:{placeholder:"积分"},model:{value:e.row.score,callback:function(a){t.$set(e.row,"score",a)},expression:"scope.row.score"}}):a("span",[t._v(t._s(e.row.score))])]}}])}),t._v(" "),a("el-table-column",{attrs:{align:"center",label:"剩余数量"},scopedSlots:t._u([{key:"default",fn:function(e){return[t.cur_index==e.row.id?a("el-input",{attrs:{placeholder:"数量"},model:{value:e.row.count,callback:function(a){t.$set(e.row,"count",a)},expression:"scope.row.count"}}):a("span",[t._v(t._s(e.row.count))])]}}])}),t._v(" "),a("el-table-column",{attrs:{"min-width":"250",prop:"rule",label:"使用规则"},scopedSlots:t._u([{key:"default",fn:function(e){return[t.cur_index==e.row.id?a("el-input",{attrs:{placeholder:"规则"},model:{value:e.row.rule,callback:function(a){t.$set(e.row,"rule",a)},expression:"scope.row.rule"}}):a("span",[t._v(t._s(e.row.rule))])]}}])}),t._v(" "),a("el-table-column",{attrs:{align:"center",label:"状态"},scopedSlots:t._u([{key:"default",fn:function(e){return[t.cur_index==e.row.id?a("div",[a("el-switch",{model:{value:e.row.state,callback:function(a){t.$set(e.row,"state",a)},expression:"scope.row.state"}})],1):a("div",[e.row.state?a("el-button",{attrs:{type:"primary",icon:"el-icon-check",size:"mini",circle:""}}):t._e(),t._v(" "),e.row.state?t._e():a("el-button",{attrs:{icon:"el-icon-close",size:"mini",circle:""}})],1)]}}])}),t._v(" "),a("el-table-column",{attrs:{fixed:"right","min-width":"95",label:"操作"},scopedSlots:t._u([{key:"default",fn:function(e){return[t.cur_index==e.row.id?a("div",[a("el-button",{attrs:{type:"text",size:"small"},on:{click:function(a){return t.handleSave(e.row)}}},[t._v("保存\n          ")]),t._v(" "),a("el-button",{attrs:{type:"text",size:"small"},on:{click:function(a){return t.handleCancel(e.row)}}},[t._v("取消\n          ")])],1):a("div",[a("el-button",{attrs:{type:"text"},on:{click:function(a){return t.handleEdit(e.row)}}},[t._v("修改\n          ")]),t._v(" "),a("el-button",{attrs:{type:"text"},on:{click:function(a){return t.handleDelete(e.row)}}},[t._v("删除\n          ")])],1)]}}])})],1),t._v(" "),a("div",{staticClass:"footer"},[a("el-pagination",{attrs:{background:"","page-size":t.page_size,layout:"prev, pager, next",total:t.total},on:{"current-change":t.currentChange}})],1)],1)},staticRenderFns:[]};var o=a("VU/8")(n,s,!1,function(t){a("mvyv")},"data-v-57192e4c",null);e.default=o.exports}});
//# sourceMappingURL=6.609d22ffc9052bbc19ae.js.map
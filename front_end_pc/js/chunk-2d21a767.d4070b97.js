(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-2d21a767"],{bc2b:function(t,n,e){"use strict";e.r(n);var i=function(){var t=this,n=t.$createElement,e=t._self._c||n;return e("com-pop",{attrs:{"my-index":"dimen-1"},scopedSlots:t._u([{key:"pop-content",fn:function(){return[e("com-head",{attrs:{company:t.company}}),e("com-content-layout",{attrs:{"get-info-list":t.infoList,"get-info-title":"工商信息","my-index":""}})]},proxy:!0},{key:"flex-left",fn:function(){},proxy:!0},{key:"flex-right",fn:function(){},proxy:!0}])})},o=[],s=(e("5118"),function(t){Promise.resolve().then(e.bind(null,"fcdb")).then(function(n){t(n)})}),a=function(t){Promise.resolve().then(e.bind(null,"b67c")).then(function(n){t(n)})},c=function(t){Promise.resolve().then(e.bind(null,"9488")).then(function(n){t(n)})},r={props:{cID:"",industryid:""},components:{ComPop:s,ComHead:a,ComContentLayout:c},data:function(){return{company:{},infoList:[]}},created:function(){this.getInfo()},watch:{"$store.state.loginInfo.showingCId":{handler:function(t){this.getInfo()}}},methods:{getInfo:function(){var t=this;this.$axios.get("".concat(this.$api.comInfo),{params:{enterpriseid:this.cID,industryid:this.industryid}}).then(function(n){var e=n.data.basic[0];if(0===n.data.code){var i=[{"企业名称":e.company_name||"未知","统一社会信用代码":e.unified_social_credit_code||"未知","注册资本":e.registered_capital||"未知","经营状态":e.status||"未知","法定代表人":e.legal_representative||"未知","登记机关":e.registration_authority||"未知","成立日期":e.established_time||"未知","类型":e.type_of_enterprise||"未知","所属行业":e.industry_involved||"未知","人员规模":e.staff_size||"未知","电话":e.phone||"未知","邮箱":e.mailbox||"未知","官网":e.official_website||"未知","企业地址":e.business_address||"未知","经营范围":e.business_scope||"未知"}];t.$store.commit("saveCompanyInfoToStore",i),t.company={name:e.company_name,LegalReprese:e.company_name,CreationTime:e.established_time,Capital:e.registered_capital},t.$set(t,"infoList",i)}})}}},f=r,u=e("2877"),d=Object(u["a"])(f,i,o,!1,null,null,null);n["default"]=d.exports}}]);
//# sourceMappingURL=chunk-2d21a767.d4070b97.js.map
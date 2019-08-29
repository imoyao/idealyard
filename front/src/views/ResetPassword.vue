<template>
  <div>
    <el-header>
      <el-menu>
        <el-menu-item>找回密码</el-menu-item>
      </el-menu>
    </el-header>
    <el-main>
      <h2>找回密码</h2>
      <el-steps :active="active" align-center>
        <el-step title="步骤1" description="输入用户注册邮箱"></el-step>
        <el-step title="步骤2" description="输入邮箱验证码 "></el-step>
        <el-step title="步骤3" description="重设密码"></el-step>
      </el-steps>
      <el-button style="margin-top: 12px;" @click="nextClick">下一步</el-button>

      <el-row  class = "active0" v-show="active === 0" >
        <div >
          <img src="static/image/data-catalog/catalog-icon1.png"/> 基本属性
        </div>

      </el-row>
      <el-row class = "active1" v-show="active === 1" > <div > <img src="static/image/data-catalog/catalog-icon1.png"/> 常规属性 </div>
      </el-row>

      <el-row class = "active2" v-show="active === 2" > <div > <img src="static/image/data-catalog/catalog-icon1.png"/> 可选属性 </div>
      </el-row>

    </el-main>


  </div>

</template>

<script>
  export default {
    name: 'ResetPassword',
    data(){
       return {
        active: 0
      };
    },
    methods: {
      goBack() {
        console.log('go back');
      },
      next() {
        if (this.active++ > 2) this.active = 0;
      },

      stepClick (val) {
        var _that = this;
        _that.active = val;
      },
      nextClick () {
        var _that= this;
        console.log(_that.active);
        if (_that.active < 3) {
          _that.active ++ ;
          console.log(_that.active);
        } else {
          _that.active = 0;
        }
      }

// 原文链接：https://blog.csdn.net/weixin_40098371/article/details/88027949

    }
  }
</script>

<style scoped>
  .me-title {
    margin-top: 10px;
  }
</style>

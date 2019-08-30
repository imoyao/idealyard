<!--此界面主要仿照豆瓣写的-->
<template>
  <div id="account">


    <div id="db-nav-sns" class="nav">
      <div class="nav-wrap">
        <div class="nav-primary">
          <el-header>
            <el-menu style="background: transparent">
              <router-link to="/" class="me-title">
                <img src="../assets/img/logo.png" alt="别院牧志">
                <h1 class="site-name">别院牧志</h1>
              </router-link>
            </el-menu>
          </el-header>
        </div>
      </div>
    </div>


    <div class="account-wrap">
      <div class="account-main">
        <h2 class="account-body-title login-label-email">
          <span class="account-body-text">找回密码</span>
        </h2>

        <el-steps :active="active" align-center style="margin-top: 20px;">
          <!--<el-step title="步骤1" icon="iconfont icon-mail" description="输入你的帐号绑定的邮箱地址"></el-step>-->
          <!--<el-step title="步骤2" icon="iconfont icon-verified" description="输入邮箱验证码 "></el-step>-->
          <!--<el-step title="步骤3" icon="iconfont icon-unlock" description="重设密码"></el-step>-->
          <el-step title="发邮件" description="输入你的帐号绑定的邮箱地址"></el-step>
          <el-step title="验证" description="输入收到的邮箱验证码 "></el-step>
          <el-step title="重设密码" description="重新设置安全认证密码"></el-step>
        </el-steps>

        <el-row class="active0 account-form" v-show="active === 0">
          <div class="account-form-raw">
            <el-form class="account-form-label" :model="emailValidateForm" ref="emailValidateForm">
              <el-form-item
                label="注册邮箱"
                prop="email"
                :rules="[{ required: true, message: '请输入注册邮箱地址'},{ type: 'email', message: '请输入正确的邮箱地址'}]">
                <el-input class="account-form-field" type="email" v-model.number="emailValidateForm.email"
                          autocomplete="off"></el-input>
              </el-form-item>
              <el-divider></el-divider>
              <el-form-item>
                <el-button type="primary" @click="submitEmail('emailValidateForm')">下一步</el-button>
                <p class="online-apply">邮箱不可用？<a target="_blank" data-action="getpwd_noemail"
                                                 href="/passport/complaint?type=reset_password" style="color:#67c23a">联系博主</a>
                </p>
              </el-form-item>
            </el-form>
          </div>
        </el-row>

        <el-row class="active1" v-show="active === 1">
          <div class="account-form-raw">
            <el-form class="account-form-label" :model="verificationCodeForm" ref="verificationCodeForm">
              <el-form-item
                label="验证码"
                prop="VerificationCode"
                :rules="[{ required: true, message: '请输入验证码'}]">
                <el-input class="account-form-field" v-model.number="verificationCodeForm.VerificationCode"
                          autocomplete="off">
                </el-input>

                <el-button @click="resendVerificationCode()">重新发送</el-button>
              </el-form-item>

              <el-divider></el-divider>

              <el-form-item>
                <el-button type="primary" @click="submitVerificationCode('verificationCodeForm')">下一步</el-button>
                <!--<el-button @click="resendVerificationCode()">重新发送</el-button>-->
              </el-form-item>
            </el-form>
          </div>
        </el-row>

        <el-row class="active2" v-show="active === 2">
          <div class="account-form-raw">
            <el-form :model="newPasswordForm" ref="newPasswordForm">
              <el-form-item
                label="新密码"
                prop="VerificationCode"
                :rules="[
            {required: true, message: '请输入密码', trigger: 'blur'},
            {max: 16, message: '不能大于 16 个字符', trigger: 'blur'},
            {min: 6, message: '不能小于 6 个字符', trigger: 'blur'},
            // {validator: prettyPw, trigger: 'blur'}
          ]">
                <el-input class="account-form-field" type="password" v-model.number="newPasswordForm.newPassword"
                          autocomplete="off"></el-input>
              </el-form-item>

              <el-divider></el-divider>

              <el-form-item>
                <el-button type="primary" @click="submitNewPassword('newPasswordForm')">确认修改</el-button>
                <!--<el-button @click="resetForm('numberValidateForm')">重置</el-button>-->
              </el-form-item>
            </el-form>
          </div>
        </el-row>

      </div>
      <div class="account-side">
        <span> &gt; </span>
        <el-link class="aside-link" href="https://support.qq.com/products/67072" target="_blank">反馈吐槽</el-link>

      </div>
    </div>

  </div>

</template>

<script>
  export default {
    name: 'ResetPassword',
    data() {
      return {
        active: 0,
        emailValidateForm: {
          email: ''
        },
        verificationCodeForm: {
          VerificationCode: ''
        },
        newPasswordForm: {
          newPassword: ''
        }
      };
    },
    methods: {
      goBack() {
        console.log('go back');
      },
      submitEmail(emailValidateForm) {
        this.$refs[emailValidateForm].validate((valid) => {
          if (valid) {
            // TODO: 验证用户邮箱
            alert('submit!');
            this.active = 1
          } else {
            console.log('error submit!!');
            return false;
          }
        });
      },
      submitVerificationCode(verificationCodeForm) {
        this.$refs[verificationCodeForm].validate((valid) => {
          if (valid) {
            // TODO: 验证邮箱验证码
            alert('submit!');
            this.active = 2
          } else {
            console.log('error submit!!');
            return false;
          }
        });
      },
      resendVerificationCode() {
        // TODO:倒计时
        alert('resend ok')
      },
      submitNewPassword(newPasswordForm) {
        this.$refs[newPasswordForm].validate((valid) => {
          if (valid) {
            // TODO: 更新用户密码
            alert('submit!');
            // TODO: 跳转到登录页
            // this.active = 3
          } else {
            console.log('error submit!!');
            return false;
          }
        });
      },
      // see also:https://blog.csdn.net/weixin_40098371/article/details/88027949


    }
  }
</script>

<style scoped>
  #db-nav-sns {
    position: relative;
    zoom: 1;
    background: #edf4ed;
  }

  #db-nav-sns .nav-primary {
    width: 1040px;
    margin: 0 auto;
    overflow: hidden;
    padding: 22px 0 20px;
    zoom: 1;
  }

  .site-name {
    display: inline-block;
    font-size: 1em;
    color: #5FB878
  }

  .me-title {
    margin-top: 10px;
    font-size: 24px;
  }

  .me-title img {
    max-height: 2.4rem;
    max-width: 100%;
  }

  .el-step__icon {
    background: #f5f5f5 !important;
  }

  .account-wrap {
    width: 1040px;
    margin: 20px auto 0;
    overflow: hidden;
  }

  .account-main {
    float: left;
    width: 590px;
  }

  .account-side {
    float: right;
    width: 310px;
    color: #666;
  }

  .account-form-raw {
    margin-top: 20px;
    margin-bottom: 20px;
    position: relative;
  }

  .account-form-field {
    position: relative;
    margin-bottom: 10px;
    width: 350px;
    display: inline-block;
  }
</style>

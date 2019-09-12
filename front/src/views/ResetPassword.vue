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
        <h2 class="account-body-title">
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

        <el-row class="email-field account-form" v-show="active === 0">
          <div class="account-form-raw">
            <el-form class="account-form-label" status-icon :model="emailValidateForm" ref="emailValidateForm">
              <el-form-item
                label="注册邮箱"
                prop="email"
                :rules="emailRules">
                <el-input class="account-form-field" type="email" v-model="emailValidateForm.email"
                          autocomplete="on"></el-input>
              </el-form-item>
              <el-divider></el-divider>
              <el-form-item>
                <el-button type="primary" @click="submitEmail('emailValidateForm')">下一步</el-button>
                <p class="online-apply">邮箱不可用？<a target="_blank" data-action="getpwd_noemail"
                                                 href="mailto:imsantu@126.com" style="color:#67c23a">联系博主</a>
                </p>
              </el-form-item>
            </el-form>
          </div>
        </el-row>

        <el-row class="captcha-field" v-show="active === 1">
          <div class="account-form-raw">
            <el-form class="account-form-label" :model="verificationCodeForm" ref="verificationCodeForm">
              <span class="captcha-ipt-tip">别院牧志向你的邮箱 {{ emailValidateForm.email }} 发送了验证码，请注意查收并及时填入。</span>
              <el-form-item
                class="captcha-ipt"
                label="验证码"
                prop="VerificationCode"
                placeholder="请输入收到的验证码"
                :rules="[{ required: true, message: '请输入验证码'}]">
                <el-input class="account-form-field" v-model="verificationCodeForm.VerificationCode" maxlength="6">
                </el-input>

                <el-button :disabled="disabled" @click="resendVerificationCode()">{{btnText}}</el-button>
              </el-form-item>

              <el-divider></el-divider>

              <el-form-item>
                <el-button type="primary" @click="submitVerificationCode('verificationCodeForm')">完成验证</el-button>
              </el-form-item>
            </el-form>
          </div>
        </el-row>

        <el-row class="password-field" v-show="active === 2">
          <div class="account-form-raw">
            <el-form :model="newPasswordForm" ref="newPasswordForm">
              <el-form-item
                label="新密码"
                prop="newPassword"
                :rules="[{required: true, message: '请输入密码', trigger: 'blur'},
                {max: 16, message: '不能大于 16 个字符', trigger: 'blur'},
                {min: 6, message: '不能小于 6 个字符', trigger: 'blur'}]">
                <el-input class="account-form-field" type="password" v-model="newPasswordForm.newPassword"
                          :show-password="true"></el-input>
              </el-form-item>

              <el-divider></el-divider>

              <el-form-item>
                <el-button type="primary" @click="submitNewPassword('newPasswordForm')">确认修改</el-button>
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
  import {fetchCheckEmail, sendCaptcha, verificateCaptcha, resetPassword, reqTaskStatus} from '@/api/login'

  export default {
    name: 'ResetPassword',
    data() {
      let checkEmail = (rule, value, callback) => {
        setTimeout(() => {
          this.syncCheckEmail(value, callback)
        }, 1000);
      };
      return {
        emailRules: [
          {required: true, message: '请输入注册邮箱地址'},
          {type: 'email', message: '请输入正确的邮箱地址'},
          {validator: checkEmail, trigger: 'blur'}
        ],
        active: 0,
        disabled: false,
        btnText: '重新发送',
        emailValidateForm:
          {
            email: ''
          }
        ,
        verificationCodeForm: {
          VerificationCode: ''
        }
        ,
        newPasswordForm: {
          newPassword: ''
        },
        mtimer: undefined,
        mailDisable: true
      };
    },
    beforeDestroy () {
      clearInterval(this.mtimer)
    },
    methods: {
      // 异步校验
      syncCheckEmail(email, callback) {
        fetchCheckEmail({email}).then((res) => {
          if (res.code === 0 && res.status === '404') {
            return callback(new Error('账户不存在'))
          } else {
            return callback()
          }
        })
      },
      getTaskStatus(taskName, location) {
        reqTaskStatus({taskName,location}).then(res => {
          let state = res.data.info.state
          this.mailDisable = state !== 'SUCCESS'
          // 成功之后清除定时器
          if (state === 'SUCCESS') {
            this.active = 1
            // this.$notify({
            //   title: i18n.t('memtest.success'),
            //   message: i18n.t('memtest.mem_test_success_tips'),
            //   position: 'bottom-right',
            //   // duration: 0,
            //   type: 'success'
            // })
            clearInterval(this.mtimer)
          }
        })
      },

      // see also:https://blog.csdn.net/weixin_40098371/article/details/88027949
      submitEmail(emailValidateForm) {
        this.$refs[emailValidateForm].validate((valid) => {
          if (valid) {
            let email = this.emailValidateForm.email
            sendCaptcha(email).then((data) => {
              let code = data.code
              // TODO:get not ok
              // this.mLocation = data.headers.Location
              // if (this.mLocation) {
              //   let that = this
              //   this.mtimer = setInterval(function () {
              //     this.getTaskStatus('mail', that.mLocation)
              //   }, 1000)
              // }
              if (code !== 0) {
                this.$message.warning({
                  message: '验证邮件发送失败！',
                })
              } else {
                this.active = 1
              }
              // https://blog.csdn.net/fabulous1111/article/details/79377654
            }).catch((error) => {
              if (error !== 'error') {
                // TODO
              }
            })

          } else {
            return false;
          }
        });
      },
      submitVerificationCode(verificationCodeForm) {
        this.$refs[verificationCodeForm].validate((valid) => {
          if (valid) {
            let email = this.emailValidateForm.email
            let captcha = this.verificationCodeForm.VerificationCode
            verificateCaptcha(email, captcha).then((data) => {
              if (data.code === 0 && data.status) {
                this.$refs.verificationCodeForm.fields[0].validateState = "error"
                this.$refs.verificationCodeForm.fields[0].validateMessage = "验证码输入错误或已过期"
              } else {
                this.active = 2
              }
              // https://blog.csdn.net/fabulous1111/article/details/79377654
            }).catch((error) => {
              if (error !== 'error') {
                console.log(error)
                // TODO
              }
            })
          } else {
            return false;
          }
        })
      },
      resendVerificationCode() {
        let email = this.emailValidateForm.email
        this.verificationCodeForm.VerificationCode = ''
        sendCaptcha(email).then((data) => {
          // https://blog.csdn.net/fabulous1111/article/details/79377654
          this.disabled = true
          // 60秒倒计时
          let time = 60
          let timer = setInterval(() => {
            if (time <= 0) {
              this.disabled = false
              this.btnText = '重新发送'
              clearInterval(timer)
            } else {
              this.btnText = time + 's 后重新发送'
              time--
            }
          }, 1000)
        }).catch((error) => {
          this.disabled = false
          if (error !== 'error') {
            console.log(error)
          }
        })
      },
      submitNewPassword(newPasswordForm) {
        this.$refs[newPasswordForm].validate((valid) => {
          if (valid) {
            let email = this.emailValidateForm.email
            let newPassword = this.newPasswordForm.newPassword
            resetPassword(email, newPassword).then((data) => {
              this.$router.go(-1)
            }).catch((error) => {
              if (error !== 'error') {
                // TODO
              }
            })
          } else {
            return false;
          }
        });
      },
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
    width: 100%;
    height: 60px;
    margin: 0 auto;
    overflow: hidden;
    padding: 22px 0 20px;
    zoom: 1;
  }

  .captcha-ipt-tip {
    font-size: 12px;
    color: #c0c4cc;
  }

  .captcha-ipt {
    margin-top: 20px;
  }

  .account-body-text {
    font-size: 0.8em;
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

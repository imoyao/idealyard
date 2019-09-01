<template>
  <div id="login" v-title data-title="登录  - 别院牧志">

    <div class="me-login-box me-login-box-radius">
      <h1>登录</h1>

      <el-form ref="userForm" :model="userForm" :rules="rules">
        <el-form-item prop="account">
          <el-input placeholder="用户名" v-model="userForm.account"></el-input>
        </el-form-item>
        <el-form-item prop="password">
          <el-input placeholder="密码" type="password" v-model="userForm.password" clearable></el-input>
        </el-form-item>
        <div class="form-text">
          <el-checkbox v-model="checked">记住密码</el-checkbox>
          <span @click="toResetPw"
                class="flr-link"><strong>找回密码</strong></span>
        </div>
        <!--<span @click="clearCookie"-->
        <!--style="cursor: pointer;color: #67c23a;font-size: 0.75rem;margin-left: 5px;float:right">重置</span>-->


        <el-form-item size="small" class="me-login-button">
          <el-button type="primary" @click.native.prevent="login('userForm')">登录</el-button>
        </el-form-item>
      </el-form>

      <div class="me-login-design">
        <p>Powered by
          <strong>
            <router-link to="/" class="me-login-design-color">IMOYAO</router-link>
          </strong>
        </p>
      </div>

    </div>
  </div>
</template>

<script>
  import {requestLogin} from '@/api/login'
  import {setToken} from '@/request/token'
  import axios from 'axios'

  export default {
    name: 'Login',
    data() {
      return {
        logining: false,
        userForm: {
          account: '',
          // account: 'imoyao',
          // password: '111111'
          password: ''
        },
        rules: {
          account: [
            {required: true, message: '请输入用户名/注册邮箱', trigger: 'blur'},
            // {max: 25, message: '不能大于25个字符', trigger: 'blur'}
          ],
          password: [
            {required: true, message: '请输入密码', trigger: 'blur'},
            // {max: 10, message: '不能大于10个字符', trigger: 'blur'}
          ]
        },
        checked: false
      }
    },
    mounted() {
      this.getCookie();
    },
    watch: {
      // 默认false，所以true时即为取消勾选
      checked(oldVal, newVal) {
        if (newVal) {
          this.clearCookie()
        }
      }
    },
    methods: {
      toResetPw() {
        this.$router.push('/reset_password')
      },
      setCookie(c_name, c_pwd, exdays) {
        let exdate = new Date(); //获取时间
        exdate.setTime(exdate.getTime() + 24 * 60 * 60 * 1000 * exdays) //保存的天数
        //字符串拼接cookie
        window.document.cookie = "userName" + "=" + c_name + ";path=/;expires=" + exdate.toGMTString()
        window.document.cookie = "password" + "=" + c_pwd + ";path=/;expires=" + exdate.toGMTString()
      },
      getCookie: function () {
        if (document.cookie.length > 0) {
          let arr = document.cookie.split('; '); //这里显示的格式需要切割一下自己可输出看下
          for (let i = 0; i < arr.length; i++) {
            let arr2 = arr[i].split('='); //再次切割
            // 判断查找相对应的值
            if (arr2[0] === 'userName') {
              this.checked = true;
              this.userForm.account = arr2[1]; //保存到保存数据的地方
            } else if (arr2[0] === 'password') {
              this.userForm.password = arr2[1];
            }
          }
        }
      },
      clearCookie: function () {
        this.userForm.password = ''
        this.setCookie("", "", -1); //修改2值都为空，天数为负1天
      },
      login(formName) {
        let that = this
        this.$refs[formName].validate((valid) => {
          if (valid) {
            if (that.checked === true) {
              //传入账号名，密码，和保存天数3个参数
              that.setCookie(that.userForm.account, that.userForm.password, 7);
            }
            this.logining = true
            // 触发vuex中的login
            that.$store.dispatch('login', that.userForm).then(() => {
              this.logining = false
              // 从哪来到哪去：see also :https://blog.csdn.net/Nalaluky/article/details/84201445
              that.$router.go(-1)
            }).catch((error) => {
              if (error !== 'error') {
                // see also:https://blog.csdn.net/lsw789/article/details/88735001
                that.$refs.userForm.fields[1].validateMessage = "请确认登录信息是否正确"
                that.$refs.userForm.fields[1].validateState  = "error"
                that.$refs.userForm.fields[0].validateState  = "error"
                // that.$message({message: error, type: 'error', showClose: true});
                this.logining = false
              }
            })
          } else {
            return false;
          }
        });
      }
    }
  }
</script>

<style scoped>
  #login {
    min-width: 100%;
    min-height: 100%;
  }

  .form-text {
    color: #67c23a;
    font-size: 0.75rem;
    margin-left: 5px;
    margin-bottom: 15px;
  }

  .flr-link {
    cursor: pointer;
    float: right;
  }

  .remember {
    margin-bottom: 20px;
  }

  .me-video-player {
    background-color: transparent;
    width: 100%;
    height: 100%;
    object-fit: fill;
    display: block;
    position: absolute;
    left: 0;
    z-index: 0;
    top: 0;
  }

  .me-login-box {
    position: absolute;
    width: 300px;
    height: 300px;
    background-color: white;
    margin-top: 150px;
    margin-left: -180px;
    left: 50%;
    padding: 30px;
  }

  .me-login-box-radius {
    border-radius: 10px;
    box-shadow: 0px 0px 1px 1px rgba(161, 159, 159, 0.1);
  }

  .me-login-box h1 {
    text-align: center;
    font-size: 24px;
    margin-bottom: 20px;
    vertical-align: middle;
  }

  .me-login-design {
    text-align: center;
    font-family: 'Open Sans', sans-serif;
    font-size: 18px;
  }

  .me-login-design-color {
    color: #5FB878 !important;
  }

  .me-login-button {
    text-align: center;
  }

  .me-login-button button {
    width: 100%;
  }

</style>

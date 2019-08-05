<template>
  <div id="login" v-title data-title="登录  - 别院牧志">

    <div class="me-login-box me-login-box-radius">
      <h1>别院牧志 登录</h1>

      <el-form ref="userForm" :model="userForm" :rules="rules">
        <el-form-item prop="account">
          <el-input placeholder="用户名" v-model="userForm.account"></el-input>
        </el-form-item>

        <el-form-item prop="password">
          <el-input placeholder="密码" type="password" v-model="userForm.password"></el-input>
        </el-form-item>

        <el-form-item size="small" class="me-login-button">
          <el-button type="primary" @click.native.prevent="login('userForm')">登录</el-button>
        </el-form-item>
      </el-form>

      <div class="me-login-design">
        <p>Designed by
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
          account: 'imoyao',
          password: '111111'
        },
        rules: {
          account: [
            {required: true, message: '请输入用户名/注册邮箱', trigger: 'blur'},
            {max: 25, message: '不能大于25个字符', trigger: 'blur'}
          ],
          password: [
            {required: true, message: '请输入密码', trigger: 'blur'},
            {max: 10, message: '不能大于10个字符', trigger: 'blur'}
          ]
        }
      }
    },
    methods: {
      login(formName) {
        let that = this

        this.$refs[formName].validate((valid) => {
          if (valid) {
            this.logining = true
            // 触发vuex中的login
            that.$store.dispatch('login', that.userForm).then(() => {
              this.logining = false
              // 从哪来到哪去：TODO:https://blog.csdn.net/Nalaluky/article/details/84201445
              that.$router.go(-1)
            }).catch((error) => {
              if (error !== 'error') {
                console.log('login',error)
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
    height: 260px;
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

<template>
  <div id="register" v-title data-title="注册  - 别院牧志">

    <div class="me-login-box me-login-box-radius">
      <h1>注册</h1>

      <el-form ref="userForm" :model="userForm" :rules="rules">
        <el-form-item prop="email">
          <el-input placeholder="邮箱地址" v-model="userForm.email"></el-input>
        </el-form-item>

        <el-form-item prop="account">
          <el-input placeholder="用户名" v-model="userForm.account"></el-input>
        </el-form-item>

        <!--<el-form-item prop="nickname">-->
        <!--<el-input placeholder="昵称" v-model="userForm.nickname"></el-input>-->
        <!--</el-form-item>-->

        <el-form-item prop="password">
          <el-input type="password" placeholder="密码" v-model="userForm.password"></el-input>
        </el-form-item>

        <el-form-item prop="rePassword">
          <el-input type="password" placeholder="重复密码" v-model="userForm.rePassword"></el-input>
        </el-form-item>

        <el-form-item size="small" class="me-login-button">
          <el-button type="primary" @click.native.prevent="register('userForm')">注册</el-button>
        </el-form-item>
      </el-form>

      <div class="me-login-design">
        <p>Powered by
          <strong>
            <router-link to="/" class="me-login-design-color">别院牧志</router-link>
          </strong>
        </p>
      </div>

    </div>
  </div>
</template>

<script>
  import {register} from '@/api/login'

  export default {
    name: 'Register',
    data() {
      let pwEqual = (rule, value, callback) => {
        if (!(this.userForm.password === this.userForm.rePassword)) {
          callback('两次填写的密码不一致')
        } else {
          callback() // 没有此处验证通过也不执行
        }
      }
      let prettyPw = (rule, value, callback) =>{
        // - 6-16 characters
        // - must contain at least 1 uppercase letter, 1 lowercase letter, and 1 number
        // - Can contain special characters
        // let pattern = /^(?=.*[0-9])(?=.*[!@#$%^&*])[a-zA-Z0-9!@#$%^&*]{6,16}$/
        let pattern = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{6,16}$/
        if (!(pattern.test(value))) {
          callback('必须包含数字、大小写字母')
        } else {
          callback()
        }
      }
      return {
        userForm: {
          email: '',
          account: '',
          nickname: '',
          password: '',
          rePassword: ''
        },
        rules: {
          email: [
            {
              required: true, //是否必填
              message: '请输入邮箱地址', //错误提示信息
              trigger: 'blur' //检验方式（blur为鼠标点击其他地方，）
            },
            {
              type: 'email',  //要检验的类型（number，email，date等）
              message: '请输入正确的邮箱地址',
              trigger: ['blur', 'change']   //change为检验的字符变化的时候
            }
          ],
          account: [
            {required: true, message: '请输入用户名', trigger: 'blur'},
            {max: 10, message: '不能大于10个字符', trigger: 'blur'}
          ],
          nickname: [
            {required: true, message: '请输入昵称', trigger: 'blur'},
            {max: 10, message: '不能大于10个字符', trigger: 'blur'}
          ],
          password: [
            {required: true, message: '请输入密码', trigger: 'blur'},
            {max: 16, message: '不能大于 16 个字符', trigger: 'blur'},
            {min: 6, message: '不能小于 6 个字符', trigger: 'blur'},
            // {validator: prettyPw, trigger: 'blur'}
          ],
          rePassword: [
            {required: true, message: '请输入确认密码', trigger: 'blur'},
            {validator: pwEqual, trigger: 'blur'}
          ]
        }

      }
    },
    methods: {
      register(formName) {
        let that = this
        this.$refs[formName].validate((valid) => {
          if (valid) {
            that.$store.dispatch('register', that.userForm).then(() => {
              that.$message({message: '注册成功 快写文章吧', type: 'success', showClose: true});
              that.$router.push({path: '/'})
            }).catch((error) => {
              if (error !== 'error') {
                that.$message({message: error, type: 'error', showClose: true});
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
    height: 320px;
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

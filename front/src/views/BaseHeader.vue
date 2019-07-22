<template>
  <el-header class="me-area">
    <el-row class="me-header">

      <el-col :span="4" class="me-header-left">
        <router-link to="/" class="me-title">
          <img src="../assets/img/logo.png"/>
        </router-link>
      </el-col>

      <el-col v-if="!simple" :span="12" :offset="2">
        <el-menu :router=true menu-trigger="click" active-text-color="#5FB878" :default-active="$route.path"
                 mode="horizontal">
          <el-menu-item index="/">首页</el-menu-item>
          <el-menu-item index="/category">分类</el-menu-item>
          <el-menu-item index="/tag">标签</el-menu-item>
          <el-menu-item index="/archives">归档</el-menu-item>
          <!--<el-menu-item index="/log">日志</el-menu-item>-->
          <el-menu-item index="/about">关于</el-menu-item>
          <!--<el-menu-item index="/messageBoard">反馈</el-menu-item>-->

          <el-col :span="2" :offset="6">
            <el-menu-item index="/write"><i class="el-icon-edit"></i>写文章</el-menu-item>
          </el-col>

        </el-menu>
      </el-col>

      <template v-else>
        <slot></slot>
      </template>

      <el-col :span="4">
        <el-menu class="transparent-header-side" :router=true menu-trigger="click" mode="horizontal" active-text-color="#5FB878">

          <template v-if="!user.login">
            <el-menu-item index="/signin">
              <el-button type="text">登录</el-button>
            </el-menu-item>
            <el-menu-item index="/register">
              <el-button type="text">注册</el-button>
            </el-menu-item>
          </template>

          <template v-else>
            <el-col :span="4" class="userinfo">
              <el-dropdown trigger="click">
                <div style="padding-left: 20px;">
                  <el-avatar :size="60" @error="errorHandler"></el-avatar>
                  <img class="me-header-picture" :src="user.avatar" />
                </div>
                <el-dropdown-menu slot="dropdown">
                  <!--<el-dropdown-item><i class="iconfont icon-bell icon-m-right"></i>我的消息</el-dropdown-item>-->
                  <el-dropdown-item><i class="iconfont icon-icon-test icon-m-right"></i>设置</el-dropdown-item>
                  <el-dropdown-item divided @click.native="logout"><i class="iconfont icon-logout icon-m-right"></i>退出</el-dropdown-item>
                </el-dropdown-menu>
              </el-dropdown>
            </el-col>
          </template>
        </el-menu>
      </el-col>

    </el-row>
  </el-header>
</template>

<script>
  import {getToken,removeToken} from '@/request/token'
  export default {
    name: 'BaseHeader',
    props: {
      activeIndex: String,
      simple: {
        type: Boolean,
        default: false
      }
    },
    data() {
      return {}
    },
    computed: {
      user() {
        let login = this.$store.state.account.length !== 0
        // let login = getToken()
        let avatar = this.$store.state.avatar
        return {
          login, avatar
        }
      }
    },
    methods: {
      errorHandler() {
        return true
      },
      // logout() {
      //   let that = this
      //   this.$store.dispatch('logout').then(() => {
      //     this.$router.push({path: '/'})
      //   }).catch((error) => {
      //     if (error !== 'error') {
      //       that.$message({message: error, type: 'error', showClose: true});
      //     }
      //   })
      // }
      logout: function () {
        let _this = this
        this.$confirm('<i>欲问后期何日是，寄书应见雁南征。</i>', '确认退出？', {
          dangerouslyUseHTMLString: true
        }).then(() => {
          // TODO: 清除工作
          removeToken()
          _this.$router.push('/signin')
        }).catch(() => {

        })
      }
    }
  }
</script>

<style>
  .transparent-header-side{
    background-color: rgba(0, 0, 0, 0);
  }
  .el-header {
    position: fixed;
    z-index: 1024;
    min-width: 100%;
    /*box-shadow: 0 2px 3px hsla(0, 0%, 7%, .1), 0 0 0 1px hsla(0, 0%, 7%, .1);*/
  }
  .userinfo {
    text-align: right;
    padding-right: 35px;
    float: right;
  }

  .me-title {
    margin-top: 10px;
    font-size: 24px;
  }

  .me-header-left {
    margin-top: 10px;
  }

  .me-title img {
    max-height: 2.4rem;
    max-width: 100%;
  }

  .me-header-picture {
    width: 36px;
    height: 36px;
    border: 1px solid #ddd;
    border-radius: 50%;
    vertical-align: middle;
    background-color: #5fb878;
    cursor: pointer;
    margin: 11px;
  }
</style>

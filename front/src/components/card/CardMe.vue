<template>
  <el-card>
    <div class="me-author-name">
      <h1 >{{ profile.username }}</h1>
      <p class="slogan-declare" align="center">
        <span style="font-size:16px"><i class="iconfont icon-heart-fill"></i>{{ profile.slogan }}</span>
      </p>
    </div>
    <el-divider></el-divider>
    <div class="profile-detail">
      <span><i class="iconfont icon-location"></i>{{ profile.location }}</span>
      &nbsp;
      <span><i class="iconfont icon-company"></i>{{profile.company }}</span>
      &nbsp;
      <span><i class="iconfont icon-idcard"></i>{{profile.occupation }}</span>
    </div>

    <div class="profile-detail">
      <i @click="showTool(qq)" :title="qq.title" class="iconfont icon-QQ"></i>
      <i @click="showTool(github)" :title="github.title" class="iconfont icon-github-fill"></i>
      <i @click="showTool(douban)" :title="douban.title" class="iconfont icon-movie"></i>
      <i @click="showTool(zhihu)" :title="zhihu.title" class="iconfont icon-zhihu"></i>
      <i @click="showTool(email)" :title="email.title" class="iconfont icon-mail"></i>
    </div>
  </el-card>

</template>

<script>
  import {isUrl} from '@/utils/regexr'
  export default {
    name: 'CardMe',
    data() {
      return {
        profile: {
          'username': '张牧志',
          'slogan': 'Valar Dohaeris.',
          'location': '鹅城',
          'company': '讲武堂',
          'occupation': '麻匪',
        },
        qq: {title: 'QQ', message: 'NDQ1NTY3ODg5'},
        github: {
          title: 'Github',
          message: 'https://github.com/imoyao'
        },
        douban: {
          title: 'Movie',
          message: 'https://movie.douban.com/people/imoyao'
        },
        zhihu: {
          title: 'Zhihu',
          message: 'https://www.zhihu.com/people/imoyao'
        },
        email: {
          title: 'Email',
          message: 'mailto:immoyao@gmail.com'
        }
      }
    },
    methods: {
      showTool(testData) {
        // 如果是链接则跳转，如果是string则显示
        const testStr = testData.message
        if (isUrl(testStr)) {
          window.open(testStr)
        }
        else{
          const _title = testData.title
          this.$message({
          title: _title,
          position:'top-right',
          dangerouslyUseHTMLString: true,
          message: '<strong>' + testStr + '</strong>',
          duration: 2000,
          offset: 150
        });
        }
      }
    }
  }
</script>

<style scoped>
  .me-author-name {
    text-align: center;
    font-size: 30px;
    border-bottom: 1px solid #5FB878;
  }

  .profile-detail {
    text-align: center;
    padding-top: 10px;
    font-size: 15px;
  }

  .profile-detail>i {
    cursor: pointer;
    padding: 4px 10px;
    font-size: 20px;
  }
</style>

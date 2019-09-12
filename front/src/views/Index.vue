<template>
  <div v-title data-title="别院牧志">
    <el-container>
      <el-main class="me-articles">
        <el-alert v-show=confirmTip.notConfirmed class="profile-alert"
          title="未完成账号验证"
          type="warning">
          <p class="el-alert__description">
            暂时无法编写文章，您必须先完成电子邮箱验证
            <br>
            您可以使用注册电子邮箱来验证身份，请前往此处进行验证。👉 &nbsp; <a @click="profile" class="profile">个人主页</a>
          </p>
        </el-alert>
        <article-scroll-page></article-scroll-page>

      </el-main>

      <el-aside>

        <card-me class="me-area"></card-me>
        <card-tag :tags="hotTags"></card-tag>

        <card-article cardHeader="最热文章" :articles="hotArticles"></card-article>

        <card-archive cardHeader="文章归档" :archives="archives"></card-archive>

        <card-article cardHeader="最新文章" :articles="newArticles"></card-article>

        <card-footer></card-footer>

      </el-aside>

    </el-container>
  </div>
</template>

<script>
  import CardMe from '@/components/card/CardMe'
  import CardArticle from '@/components/card/CardArticle'
  import CardArchive from '@/components/card/CardArchive'
  import CardTag from '@/components/card/CardTag'
  import CardFooter from '@/components/card/CardFooter'
  import ArticleScrollPage from '@/views/common/ArticleScrollPage'

  import {reqArticles, reqHotArtices, reqNewArtices} from '@/api/article'
  import {reqHotTags} from '@/api/tag'
  import {listArchives} from '@/api/article'

  export default {
    name: 'Index',
    created() {
      this.getHotArticles()
      this.getNewArtices()
      this.getHotTags()
      this.listArchives()
    },
    data() {
      return {
        hotTags: [],
        hotArticles: [],
        newArticles: [],
        archives: []
      }
    },
    computed: {
      confirmTip() {
        let login = false
        if (this.$store.state.account){
          login = this.$store.state.account.length !== 0
        }
        let confirmed = this.$store.state.confirmed
        let notConfirmed = !confirmed && login
        return {
          notConfirmed
        }
      }
    },
    methods: {
      profile(){
        this.$router.push('/profile')
      },
      getHotArticles() {
        let that = this
        reqHotArtices().then(data => {
          that.hotArticles = data.data
        }).catch(error => {
          if (error !== 'error') {
            console.log(error)
            // that.$message.error({message: '最热文章加载失败!', showClose: true})
          }
        })
      },
      getNewArtices() {
        let that = this
        reqNewArtices().then(data => {
          that.newArticles = data.data
        }).catch(error => {
          if (error !== 'error') {
            console.log(error)
            // that.$message.error({message: '最新文章加载失败!', showClose: true})
          }
        })
      },
      getHotTags() {
        let that = this
        reqHotTags().then(data => {
          that.hotTags = data.data
        }).catch(error => {
          if (error !== 'error') {
            console.log(error)
            // that.$message.error({message: '最热标签加载失败!', showClose: true})
          }
        })
      },
      listArchives() {
        listArchives().then((data => {
          this.archives = data.data
        })).catch(error => {
          if (error !== 'error') {
            console.log(error)
            // this.$message.error({message: '文章归档加载失败!', showClose: true})
          }
        })
      }
    },
    components: {
      'card-me': CardMe,
      'card-article': CardArticle,
      'card-tag': CardTag,
      'card-footer': CardFooter,
      ArticleScrollPage,
      CardArchive
    }
  }
</script>

<style scoped>

  .el-container {
    width: 960px;
  }

  .el-aside {
    margin-left: 20px;
    width: 260px;
  }

  .el-main {
    padding: 0px;
    line-height: 16px;
  }

  .el-card {
    border-radius: 0;
  }

  .el-card:not(:first-child) {
    margin-top: 20px;
  }

  .profile-alert{
    margin-bottom: 15px;
    border-color: #E6A23C;
    box-shadow: 0 1px 3px rgba(26,26,26,.1);
  }
  .profile{
    color:#409EFF;
  }
  .profile:hover{
    color:#67c23a;
  }
</style>

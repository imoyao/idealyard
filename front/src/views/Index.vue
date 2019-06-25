<template>
  <div v-title data-title="别院牧志">
    <el-container>

      <el-main class="me-articles">
        <p>这里显示文章列表</p>

        <article-scroll-page></article-scroll-page>

      </el-main>

      <el-aside>

        <card-me class="me-area"></card-me>
        <card-tag :tags="hotTags"></card-tag>

        <card-article cardHeader="最热文章" :articles="hotArticles"></card-article>

        <card-archive cardHeader="文章归档" :archives="archives"></card-archive>

        <card-article cardHeader="最新文章" :articles="newArticles"></card-article>

      </el-aside>

    </el-container>
  </div>
</template>

<script>
  import CardMe from '@/components/card/CardMe'
  import CardArticle from '@/components/card/CardArticle'
  import CardArchive from '@/components/card/CardArchive'
  import CardTag from '@/components/card/CardTag'
  import ArticleScrollPage from '@/views/common/ArticleScrollPage'

  import {reqArticles, reqHotArtices, reqNewArtices, reqArchives} from '@/api/article'
  import {reqHotTags} from '@/api/tag'
  // TODO,token认证方式
  // https://segmentfault.com/a/1190000011277435
  export default {
    name: 'Index',
    data: function () {
      return {
        msg: "",
        hotTags: [],
        hotArticles: [],
        newArticles: [],
        archives: []
      }
    },
    methods: {
      // 最热文章
      getHotArtices() {
        let that = this
        reqHotArtices().then(data => {
          that.hotArticles = data.data
        }).catch(error => {
          if (error !== 'error') {
            that.$message({type: 'error', message: '最热文章加载失败!', showClose: true})
          }

        })

      },
      getNewArtices() {
        let that = this
        reqNewArtices().then(data => {
          that.newArticles = data.data
        }).catch(error => {
          if (error !== 'error') {
            that.$message({type: 'error', message: '最新文章加载失败!', showClose: true})
          }

        })

      },
      getHotTags() {
        let that = this
        reqHotTags().then(data => {
          that.hotTags = data.data
        }).catch(error => {
          if (error !== 'error') {
            that.$message({type: 'error', message: '最热标签加载失败!', showClose: true})
          }

        })
      },
      listArchives() {
        reqArchives().then((data => {
          this.archives = data.data
        })).catch(error => {
          if (error !== 'error') {
            this.$message({type: 'error', message: '文章归档加载失败!', showClose: true})
          }
        })
      },
      logout() {
        this.$store.commit('delToken')
        this.$router.push('/login')
      }
    },
    created() {
      // this.$axios.get("/").then(response => {
      //   this.msg = response.data
      // }).catch(error => {
      //   console.log(error)
      //   this.$Message.error(error)
      // })
      // 页面完成之前获取到这些信息
      this.getHotArtices()
      this.getNewArtices()
      this.getHotTags()
      this.listArchives()
    },
    // 组件
    components: {
      'card-me': CardMe,
      'card-article': CardArticle,
      'card-tag': CardTag,
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
</style>

<template>
  <div v-title :data-title="title">
    <el-container >
        <el-aside class="me-area" v-if="archives">
          <!--TODO:此处获取数据失败时表现怪异-->
          <p></p>
          <ul class="me-month-list">
            <li v-for="( a, index ) in archives" :key="index" class="me-month-item">
              <el-badge :value="a.counts">
                <el-button @click="changeArchive(a.year, a.month)" size="small">{{a.year +'年' + a.month + '月'}}
                </el-button>
              </el-badge>
            </li>
          </ul>

        </el-aside>

      <el-main class="me-articles">
        <div class="me-month-title">{{currentArchive}}</div>
        <!--TODO:如果去掉注释me-area，此处表现怪异-->
        <!--没有的时候，应该在此处显示内容-->

        <article-scroll-page v-bind="article"></article-scroll-page>

      </el-main>
    </el-container>
  </div>

</template>

<script>
  import ArticleScrollPage from '@/views/common/ArticleScrollPage'
  import {listArchives} from '@/api/article'

  export default {
    name: "BlogArchive",
    components: {
      ArticleScrollPage
    },
    created() {
      this.listArchives()
    },
    watch: {
      '$route'() {
        if (this.$route.params.year && this.$route.params.month) {
          this.article.query.year = this.$route.params.year
          this.article.query.month = this.$route.params.month
        }
      }
    },
    data() {
      return {
        article: {
          query: {
            month: this.$route.params.month,
            year: this.$route.params.year
          }
        },
        archives: []
      }
    },
    computed: {
      title (){
        return this.currentArchive + ' - 文章归档 - For Fun'
        // # TODO 组装成的！！！
      },
      currentArchive (){
        // 获取为空
        if (this.archives.length === 0){
          // TODO: 打开太快，它出来了
          return 'Oh no 😢'
        } else if (this.article){
          if(this.article.query.year && this.article.query.month){
          return `${this.article.query.year}年${this.article.query.month}月`
        }
        return '全部'
        }
      }
    },
    methods: {

      changeArchive(year, month) {
        console.log('---------','changeArchive')
        // this.currentArchive = `${year}年${month}月`
        // this.article.query.year = year
        // this.article.query.month = month
        this.$router.push({path: `/archives/${year}/${month}`})
      },
      listArchives() {
        listArchives().then((data => {
          this.archives = data.data
        })).catch(error => {
          this.$message({type: 'error', message: '文章归档加载失败!', showClose: true})
        })
      }
    },
  }
</script>

<style scoped>

  .el-container {
    width: 640px;
  }

  .el-aside {
    position: fixed;
    left: 200px;
    margin-right: 50px;
    width: 150px !important;
  }

  .el-main {
    padding: 0px;
    line-height: 16px;
  }

  .me-month-list {
    margin-top: 10px;
    margin-bottom: 10px;
    text-align: center;
    list-style-type: none;
  }

  .me-month-item {
    margin-top: 18px;
    padding: 4px;
    font-size: 18px;
    color: #5FB878;
  }

  .me-order-list {
    float: right;
  }

  .me-month-title {
    margin-left: 4px;
    margin-top: 10px;
    margin-bottom: 12px;
  }
</style>

<template>
  <div class="me-view-body" v-title :data-title="title">
    <el-container class="me-view-container">
      <el-main>
        <div class="me-view-card">
          <h1 class="me-view-title">{{article.title}}</h1>
          <div class="me-view-author">
            <a class="">
              <img class="me-view-picture" :src="article.author.avatar"></img>
            </a>
            <div class="me-view-info">
              <span>{{article.author.nickname}}</span>
              <div class="me-view-meta">
                <span>{{article.createDate | format}}</span>
                <span>阅读   {{viewCount}}</span>
                <span>评论   {{article.commentCounts}}</span>
              </div>

            </div>

          </div>
          <div class="me-view-content">
            <markdown-editor :editor=article.editor></markdown-editor>
          </div>

          <div>
            <el-divider><span>正文结束</span></el-divider>
          </div>

          <div class="me-view-tag">
            标签：
            <!--<el-tag v-for="t in article.tags" :key="t.id" class="me-view-tag-item" size="mini" type="success">{{t.tagname}}</el-tag>-->

            <el-button @click="tagOrCategory('tag', t.id)" size="mini" type="primary" v-for="t in article.tags"
                       :key="t.id" round plain>{{t.tagname}}
            </el-button>
          </div>

          <div class="me-view-tag">
            分类：
            <!--<span style="font-weight: 600">{{article.category.categoryname}}</span>-->
            <el-button @click="tagOrCategory('category', article.category.id)" size="mini" type="primary" round plain>
              {{article.category.categoryname}}
            </el-button>
          </div>
          <div class="me-view-tag">
            更新于：
            <el-tag type="warning">{{article.updateDate | format}}</el-tag>
          </div>
          <el-button-group style="position: absolute;left: 60%;" v-if="this.article.author.id === this.$store.state.id">
            <el-button @click="editArticle()" size="mini" type="primary" icon="el-icon-edit" plain></el-button>
            <!--<el-button @click="btnVisable()" size="mini" type="primary" icon="el-icon-share" plain></el-button>-->
            <el-button @click="delArticle()" size="mini" type="danger" icon="el-icon-delete" plain></el-button>
          </el-button-group>

          <div class="me-view-comment">
            <div class="me-view-comment-write">
              <el-row :gutter="20">
                <el-col :span="2">
                  <a class="">
                    <img class="me-view-picture" :src="avatar"></img>
                  </a>
                </el-col>
                <el-col :span="22">
                  <el-input
                    type="textarea"
                    :autosize="{ minRows: 2}"
                    placeholder="你的评论..."
                    class="me-view-comment-text"
                    v-model="comment.content"
                    resize="none">
                  </el-input>
                </el-col>
              </el-row>

              <el-row :gutter="20">
                <el-col :span="2" :offset="22">
                  <el-button type="text" @click="publishComment()">评论</el-button>
                </el-col>
              </el-row>
            </div>

            <div class="me-view-comment-title">
              <span>{{article.commentCounts}} 条评论</span>
            </div>

            <commment-item
              v-for="(c,index) in comments"
              :comment="c"
              :articleId="article.id"
              :index="index"
              :rootCommentCounts="comments.length"
              @commentCountsIncrement="commentCountsIncrement"
              :key="c.id">
            </commment-item>

          </div>

        </div>
      </el-main>

    </el-container>
  </div>
</template>

<script>
  import MarkdownEditor from '@/components/markdown/MarkdownEditor'
  import CommmentItem from '@/components/comment/CommentItem'
  import {viewArticle, identiferArticle, patchCount, identiferCount, deleteArticle, reqPostid} from '@/api/article'
  import {reqCommentsByArticle, publishComment} from '@/api/comment'

  import default_avatar from '@/assets/img/default_avatar.png'

  export default {
    name: 'BlogView',
    // beforeCreate(){
    //   this.getPostId()
    // },
    // TODO: created 中的函数使用then异步执行应该也可以
    created() {
      this.getPostId().then(
        this.getArticle()
      )
      this.addReadCount()
      this.btnVisable()
    },
    watch: {
      '$route': 'getArticle'
    },
    data() {
      return {
        visable: Boolean,
        viewCount: 0,
        postId: '',
        article: {
          id: String,
          identifier: String,
          slug: String,
          title: '',
          commentCounts: 0,
          viewCounts: 0,
          summary: '',
          author: {},
          tags: [],
          category: {},
          createDate: '',
          editor: {
            value: '',
            toolbarsFlag: false,
            subfield: false,
            defaultOpen: 'preview'
          }
        },
        comments: [],
        comment: {
          article: {},
          content: ''
        }
      }
    },
    computed: {
      avatar() {
        let avatar = this.$store.state.avatar

        if (avatar.length > 0) {
          return avatar
        }
        return default_avatar
      },
      title() {
        return `${this.article.title} - 文章  - 别院牧志`
      }
    },
    methods: {
      // getPostId(){
      //   let identifier = this.$route.params.identifier
      //   reqPostid(identifier).then(data => {
      //     this.postId = data.data.postId
      //   })
      // },
      getPostId() {
        return new Promise((resolve, reject) => {
          let identifier = this.$route.params.identifier
          reqPostid(identifier).then((data) => {
            this.postId = data.data.postId
            resolve()
          }).catch((error) => {
            reject(error)
          })
        })
      },
      addReadCount: function() {
        let that = this
        if (this.postId){
          patchCount(this.postId).then(data => {
            this.viewCount = data.data.count
          })
        }else{
          let postIdentifier = that.$route.params.identifier
          identiferCount(postIdentifier).then(data => {
            this.viewCount = data.data.count
          })
        }

      },
      tagOrCategory(type, id) {
        this.$router.push({path: `/${type}/${id}`})
      },
      editArticle() {
        this.$router.push({path: `/write/${this.article.id}`})
      },
      delArticle() {
        this.$confirm('此操作将永久删除该文章, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          let postId = this.article.id
          let authorId = this.article.author.id
          deleteArticle(postId, authorId).then(data => {
            this.$message.success({
              type: 'success',
              message: '删除成功!'
            });
            this.$router.push({path: '/'})
          }).catch(error => {
            if (error !== 'error') {
              this.$message.error({message: '文章删除失败', showClose: true})
            }
          })
        }).catch(() => {
          this.$message.info({
            message: '已取消删除'
          });
        });
      },
      getArticle () {
        let that = this
        this.postId = that.$route.params.id
        let postIdentifier = that.$route.params.identifier
        // 此处为了url更好看，将identifier传到后台拿回id，因为params的值在用户刷新页面后会丢失，
        // 而query方式传参会导致url看起来像get请求，不够优雅，没有好的办法，只能暂时这样处理
        if (this.postId) {
          viewArticle(this.postId).then(data => {
            Object.assign(that.article, data.data)
            if (!this.postId) {
              this.postId = data.data.id
            }
            that.article.editor.value = data.data.body.content
            that.article.editor.value = data.data.body.content
            that.article.author.id = data.data.author.id
            that.getCommentsByArticle()
          }).catch(error => {
            if (error !== 'error') {
              that.$message.error({message: '文章加载失败', showClose: true})
            }
          })
        } else {
          identiferArticle(postIdentifier).then(data => {
            Object.assign(that.article, data.data)
            if (!this.postId) {
              this.postId = data.data.id
            }
            that.article.editor.value = data.data.body.content
            that.article.editor.value = data.data.body.content
            that.article.author.id = data.data.author.id
            that.getCommentsByArticle()
          }).catch(error => {
            if (error !== 'error') {
              that.$message.error({message: '文章加载失败', showClose: true})
            }
          })
        }
      },
      publishComment() {
        let that = this
        if (!that.comment.content) {
          return;
        }
        that.comment.article.id = that.article.id
        publishComment(that.comment).then(data => {
          that.$message.success({message: '评论成功', showClose: true})
          that.comments.unshift(data.data)
          that.commentCountsIncrement()
          that.comment.content = ''
        }).catch(error => {
          if (error !== 'error') {
            that.$message.error({message: '评论失败', showClose: true})
          }
        })
      },
      getCommentsByArticle() {
        let that = this
        reqCommentsByArticle(that.article.id).then(data => {
          that.comments = data.data
        }).catch(error => {
          if (error !== 'error') {
            that.$message.error({message: '评论加载失败', showClose: true})
          }
        })
      },
      commentCountsIncrement() {
        this.article.commentCounts += 1
      },
      // TODO: 获取不到？
      btnVisable() {
        this.visable = this.article.author.id === this.$store.state.id
      }
    },
    components: {
      'markdown-editor': MarkdownEditor,
      CommmentItem
    },
    //组件内的守卫 调整body的背景色
    beforeRouteEnter(to, from, next) {
      window.document.body.style.backgroundColor = '#fff';
      next();
    },
    beforeRouteLeave(to, from, next) {
      window.document.body.style.backgroundColor = '#f5f5f5';
      next();
    }
  }
</script>

<style>
  .me-view-body {
    margin: 100px auto 140px;
  }

  .me-view-container {
    width: 700px;
  }

  .el-main {
    overflow: hidden;
  }

  .me-view-title {
    font-size: 34px;
    font-weight: 700;
    line-height: 1.3;
  }

  .me-view-author {
    margin-top: 30px;
    vertical-align: middle;
  }

  .me-view-picture {
    width: 40px;
    height: 40px;
    border: 1px solid #ddd;
    border-radius: 50%;
    vertical-align: middle;
    background-color: #5fb878;
  }

  .me-view-info {
    display: inline-block;
    vertical-align: middle;
    margin-left: 8px;
  }

  .me-view-meta {
    font-size: 12px;
    color: #969696;
  }

  .me-view-end {
    margin-top: 20px;
  }

  .me-view-tag {
    margin-top: 20px;
    padding-left: 6px;
    border-left: 4px solid #c5cac3;
  }

  .me-view-tag-item {
    margin: 0 4px;
  }

  .me-view-comment {
    margin-top: 60px;
  }

  .me-view-comment-title {
    font-weight: 600;
    border-bottom: 1px solid #f0f0f0;
    padding-bottom: 20px;
  }

  .me-view-comment-write {
    margin-top: 20px;
  }

  .me-view-comment-text {
    font-size: 16px;
  }

  .v-show-content {
    padding: 8px 25px 15px 0px !important;
  }

  .v-note-wrapper .v-note-panel {
    box-shadow: none !important;
  }

  .v-note-wrapper .v-note-panel .v-note-show .v-show-content, .v-note-wrapper .v-note-panel .v-note-show .v-show-content-html {
    background: #fff !important;
  }

  blockquote {
    background-color: #fff6f7;
    border-radius: 4px;
    border-left: 5px solid #fe6c6f !important;
    margin: 1rem 10px !important;
    padding: .5em 10px !important;
    quotes: "\201C" "\201D" "\2018" "\2019" !important;
    font-family: 'Open Sans', "Helvetica Neue", "Helvetica", "Microsoft YaHei", "WenQuanYi Micro Hei", Arial, sans-serif
  }

  .el-divider__text {
    position: absolute;
    background-color: #fff;
    padding: 0 20px;
    font-weight: 500;
    color: #cc2a41;
    font-size: 14px;
  }

</style>

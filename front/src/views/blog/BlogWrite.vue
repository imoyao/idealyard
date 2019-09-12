<template>
  <div id="write" v-title :data-title="title">
    <el-container>
      <base-header :simple=true>
        <el-col :span="6" :offset="2">
          <div class="me-write-info">写文章</div>
        </el-col>
        <el-col :span="4" :offset="3">
          <el-button-group class="me-write-btn">
            <el-button icon="el-icon-upload" size="small" round :autofocus="true" @click="publishShow">发布</el-button>
            <el-button icon="el-icon-delete" size="small" round @click="cancel">取消</el-button>
          </el-button-group>
        </el-col>
      </base-header>

      <el-container class="me-area me-write-box">
        <el-main class="me-write-main">
          <div class="me-write-title">
            <el-input resize="none"
                      type="textarea"
                      autosize
                      v-model="articleForm.title"
                      placeholder="请输入标题"
                      class="me-write-input">
            </el-input>

          </div>
          <div id="placeholder" style="visibility: hidden;height: 89px;display: none;"></div>
          <markdown-editor :editor="articleForm.editor" class="me-write-editor"></markdown-editor>
        </el-main>
      </el-container>

      <el-dialog title="摘要 | 分类 | 置顶 | 链接 | 标签"
                 :visible.sync="publishVisible"
                 :close-on-click-modal=false
                 custom-class="me-dialog">
        <el-form :model="articleForm" ref="articleForm" :rules="rules">
          <el-form-item label="文章摘要" prop="summary" class="iy-slug-ipt">
            <el-input
              type="textarea"
              v-model="articleForm.summary"
              style="display:flex !important;width:85%;"
              :autosize="{ minRows: 2, maxRows: 8}"
              placeholder="请输入摘要">
            </el-input>
          </el-form-item>
          <el-form-item label="文章分类" prop="category">
            <!--https://element.eleme.cn/#/zh-CN/component/select#chuang-jian-tiao-mu-->
            <el-select
              v-model="articleForm.category"
              filterable
              allow-create
              default-first-option
              placeholder="请选择文章分类">
              <el-option
                v-for="item in categories"
                :key="item.id"
                :label="item.categoryname"
                :value="item.categoryname">
              </el-option>

            </el-select>
            <el-tooltip class="item" effect="dark" content="你可以点击选择已有分类或者为文章创建新分类" placement="right">
              <i class="iconfont icon-question-circle"></i>
            </el-tooltip>
          </el-form-item>
          <el-form-item label="文章置顶" prop="weight">
            <el-switch style="margin-left: 8px;" v-model="topPost">
            </el-switch>
          </el-form-item>

          <!-- 更新时此输入框应为不可见-->
          <el-form-item label="英文链接" prop="slug" v-if="newPost">
            <el-autocomplete
              class="iy-slug-ipt"
              v-model="articleForm.slug"
              autosize
              :maxlength="60"
              show-word-limit
              :fetch-suggestions="querySearchAsync"
              placeholder="请输入英文标题"
              @select="handleSelect">
              <el-button slot="append" icon="iconfont icon-translate"></el-button>
            </el-autocomplete>
            <el-tooltip class="item" effect="dark" content="你可以为文章自定义一个简短优雅的英文标题以创建链接" placement="right">
              <i class="iconfont icon-question-circle"></i>
            </el-tooltip>
          </el-form-item>

          <el-form-item label="文章标签" prop="tags">
            <el-tooltip class="item" effect="dark" placement="right">
              <div slot="content">你可以选择删除已有标签然后点击按钮为文章创建新标签<br>（多个标签支持以逗号、空格分割批量添加）</div>
              <i class="iconfont icon-question-circle"></i>
            </el-tooltip>
            <br>
            <el-tag
              :key="tag"
              v-for="tag in dynamicTags"
              closable
              :disable-transitions="false"
              @close="handleClose(tag)">
              {{tag}}
            </el-tag>
            <el-input
              class="input-new-tag"
              v-if="inputVisible"
              v-model="inputValue"
              ref="saveTagInput"
              size="small"
              @keyup.enter.native="handleInputConfirm"
              @blur="handleInputConfirm"
            >
            </el-input>
            <!--TODO:添加清空所有的按钮-->
            <el-button v-else class="button-new-tag" size="small" @click="showInput">+ 创建标签</el-button>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button-group>
            <el-button type="primary" @click="publish('articleForm')" icon="el-icon-upload">发布</el-button>
            <el-button @click="publishVisible = false" icon="el-icon-delete">取 消</el-button>
          </el-button-group>
        </div>
      </el-dialog>
    </el-container>
  </div>
</template>

<script>
  import { fix as fixSpace } from 'lint-md';

  import BaseHeader from '@/views/BaseHeader'
  import MarkdownEditor from '@/components/markdown/MarkdownEditor'
  import {publishArticle, reqArticleById, updateArticle, reqArticleSlug} from '@/api/article'
  import {reqAllCategories} from '@/api/category'
  import {reqMostTags} from '@/api/tag'

  export default {
    name: 'BlogWrite',
    mounted() {
      if (this.$route.params.id) {
        this.getArticleById(this.$route.params.id)
      }
      this.getCategorysAndTags()
      this.editorToolBarToFixedWrapper = this.$_.throttle(this.editorToolBarToFixed, 200)
      window.addEventListener('scroll', this.editorToolBarToFixedWrapper, false)
      // 弹窗提示
      window.onbeforeunload = function (e) {
        e = e || window.event
        // 兼容IE8和Firefox 4之前的版本
        if (e) {
          e.returnValue = '关闭提示'
        }
        // Chrome, Safari, Firefox 4+, Opera 12+ , IE 9+
        return '关闭提示'
      }
    },
    beforeDestroy() {
      window.removeEventListener('scroll', this.editorToolBarToFixedWrapper, false)
    },
    data() {
      return {
        topPost: false,
        postSaved: false,
        newPost: true,
        postTitle: '',
        options: [{
          value: 'HTML',
          label: 'HTML'
        }, {
          value: 'CSS',
          label: 'CSS'
        }, {
          value: 'JavaScript',
          label: 'JavaScript'
        }],
        dynamicTags: [],
        inputVisible: false,
        inputValue: '',
        publishVisible: false,
        userVisableTags: [],
        categories: [],
        articleForm: {
          id: '',
          title: '',
          summary: '',
          category: '',
          slug: '',
          tags: [],
          editor: {
            value: '',
            ref: '',//保存mavonEditor实例  实际不该这样
            default_open: 'edit',
            placeholder: '唯有文字能担当此任，宣告生命曾经在场。',
            toolbars: {
              bold: true, // 粗体
              italic: true, // 斜体
              header: true, // 标题
              underline: true, // 下划线
              strikethrough: true, // 中划线
              mark: true, // 标记
              superscript: true, // 上角标
              subscript: true, // 下角标
              quote: true, // 引用
              ol: true, // 有序列表
              ul: true, // 无序列表
              imagelink: true, // 图片链接
              code: true, // code
              fullscreen: true, // 全屏编辑
              readmodel: true, // 沉浸式阅读
              help: true, // 帮助
              undo: true, // 上一步
              redo: true, // 下一步
              trash: true, // 清空
              navigation: true, // 导航目录
              //subfield: true, // 单双栏模式
              preview: true, // 预览
            }
          }
        },
        rules: {
          summary: [
            {required: true, message: '请输入摘要', trigger: 'blur'},
            {max: 200, message: '不能大于 200 个字符', trigger: 'blur'}
          ],
          category: [
            {required: true, message: '请选择文章分类', trigger: 'change'}
          ],
          tags: [
            // {type: 'array', required: true, message: '请选择标签', trigger: 'change'}
            {type: 'array', message: '请选择标签', trigger: 'change'}
          ]
        }
      }
    },
    computed: {
      title() {
        return '写文章  - 别院牧志'
      }
    },
    methods: {
      // https://blog.csdn.net/qq_37746973/article/details/78402812
      querySearchAsync(queryString, cb) {
        console.log(this.postTitle)
        reqArticleSlug(this.postTitle).then(data => {
          let slug = data.data
          let slugList = [{"value": slug}]
          cb(slugList)
        })
      },
      handleSelect(item) {
      },
      handleClose(tag) {
        this.dynamicTags.splice(this.dynamicTags.indexOf(tag), 1);
      },
      showInput() {
        this.inputVisible = true;
        this.$nextTick(_ => {
          this.$refs.saveTagInput.$refs.input.focus();
        });
      },
      // see:https://www.jianshu.com/p/24f3320d3d40
      handleInputConfirm() {
        let inputValue = this.inputValue;
        if (inputValue) {
          // 对用户输入值进行切分
          let values = inputValue.split(/[,， \n]/).filter(item => {
            return item !== '' && item !== undefined
          })
          // 对列表索引，没有找到则push
          values.forEach(element => {
            let index = this.dynamicTags.findIndex(i => {
              return i === element
            })
            if (index < 0) {
              this.dynamicTags.push(element);
            }
          });
        }
        // 添加完成自动消失
        this.inputVisible = false;
        this.inputValue = '';
      },
      getArticleById(id) {
        let that = this
        reqArticleById(id).then(data => {
          Object.assign(that.articleForm, data.data)
          that.articleForm.editor.value = data.data.body.content
          that.articleForm.summary = data.data.body.summary
          that.articleForm.category = data.data.category.categoryname
          that.articleForm.slug = data.data.slug
          that.topPost = data.data.weight === 1
          let postTags = this.articleForm.tags.map(function (item) {
            return item.tagname;
          })
          this.articleForm.tags = postTags
          this.dynamicTags = postTags

        }).catch(error => {
          if (error !== 'error') {
            that.$message.error({message: '文章加载失败', showClose: true})
          }
        })
      },
      publishShow() {
        this.postTitle = this.articleForm.title
        // 更新文章时，添加英文标题的一行不可见
        this.newPost = !this.articleForm.id
        if (!this.articleForm.title) {
          this.$message.warning({message: '标题不能为空哦 👀', showClose: true})
          return
        }

        if (this.articleForm.title.length > 30) {
          this.$message.warning({message: '标题不能大于30个字符', showClose: true})
          return
        }

        if (!this.articleForm.editor.ref.d_render) {
          this.$message.warning({message: '内容要满满的诚意哦 😜', showClose: true})
          return
        }

        this.publishVisible = true;
      },
      publish(articleForm) {
        let that = this
        this.$refs[articleForm].validate((valid) => {
          if (valid) {
            // TODO:重复
            this.articleForm.tags.map(function (item) {
              return item.tagname;
            });
            const panTitle = fixSpace(this.articleForm.title);
            const panSummary = fixSpace(this.articleForm.summary);
            const panContent = fixSpace(this.articleForm.editor.value);
            let article = {
              // 带上用户信息
              authorId: this.$store.state.id,
              id: this.articleForm.id,
              title: panTitle,
              summary: panSummary,
              category: this.articleForm.category,
              slug: this.articleForm.slug,
              dynamicTags: this.dynamicTags,
              tags: this.articleForm.tags,
              weight: this.topPost,
              body: {
                content: panContent,
                contentHtml: this.articleForm.editor.ref.d_render
              }

            }
            // 关闭发布框
            this.publishVisible = false
            this.postSaved = true
            let loading = this.$loading({
              lock: true,
              text: '发布中，请稍后...'
            })
            let postId = article.id
            // 编辑文章
            if (postId) {
              updateArticle(article).then((data) => {
                loading.close();
                that.$message.success({message: '文章更新成功', showClose: true})
                let identifier = data.data.identifier
                let slug = data.data.slug
                that.$router.push({path: `/posts/${identifier}/${slug}`})
              }).catch((error) => {
                loading.close();
                if (error !== 'error') {
                  console.log(error)
                  // that.$message.error({message: error, showClose: true});
                }
              })
            } else {    // 发表文章
              publishArticle(article).then((data) => {
                loading.close()
                that.$message.success({message: '发布成功啦', showClose: true})
                let identifier = data.data.identifier
                let slug = data.data.slug
                that.$router.push({path: `/posts/${identifier}/${slug}`})
              }).catch((error) => {
                loading.close()
                if (error !== 'error') {
                  that.$message.error({message: error, showClose: true})
                }
              })
            }
          } else {
            return false;
          }
        });
      },
      cancel() {
        this.$confirm('文章将不会保存, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          window.onbeforeunload = null
          this.$router.push('/')
        })
      },
      getCategorysAndTags() {
        let that = this
        reqAllCategories().then(data => {
          that.categories = data.data
        }).catch(error => {
          if (error !== 'error') {
            that.$message.error({message: '文章分类加载失败', showClose: true})
          }
        })
        // console.log('edit-or-new', this.$route.params.id)
        let postId = this.$route.params.id
        let tagData = Object()
        // 有id时上面已经获取到了
        if (!postId) {
          // 只显示热门标签，没有必要把所有标签都列出来，让用户可以自主添加更好
          tagData = reqMostTags().then(data => {
            that.tags = data.data
            that.tags.forEach(tag => {
              // 保存用户最终添加的tags
              this.dynamicTags.push(tag.tagname)
              // 保存用户可见tags
              this.userVisableTags.push(tag.tagname)
            })
          }).catch(error => {
            if (error !== 'error') {
              that.$message.error({message: '标签加载失败', showClose: true})
            }
          })
        }
      },
      editorToolBarToFixed() {
        let toolbar = document.querySelector('.v-note-op');
        let curHeight = document.documentElement.scrollTop || document.body.scrollTop;
        if (curHeight >= 160) {
          document.getElementById("placeholder").style.display = "block"; //bad  用计算属性较好
          toolbar.classList.add("me-write-toolbar-fixed");
        } else {
          document.getElementById("placeholder").style.display = "none";
          toolbar.classList.remove("me-write-toolbar-fixed");
        }
      }
    },
    components: {
      'base-header': BaseHeader,
      'markdown-editor': MarkdownEditor
    },
    //组件内的守卫 调整body的背景色
    beforeRouteEnter(to, from, next) {
      window.document.body.style.backgroundColor = '#fff';
      next();
    },
    // see also: https://www.haorooms.com/post/single_page_refrashtips
    // https://juejin.im/entry/5bebc4b3e51d4575125a39bb
    beforeRouteLeave(to, from, next) {
      let userEnter = this.articleForm.title || this.articleForm.editor.value
      if (!userEnter || this.postSaved) {
        next()
        return true
      }
      let answer = window.confirm('当前页面数据未保存，确定要离开？')
      if (answer) {
        window.document.body.style.backgroundColor = '#f5f5f5'
        next()
      } else {
        next(false)
      }
    },
    destroyed() {
      window.onbeforeunload = null
    }
  }
</script>

<style>
  .el-header {
    position: fixed;
    z-index: 1024;
    min-width: 100%;
    box-shadow: 0 2px 3px hsla(0, 0%, 7%, .1), 0 0 0 1px hsla(0, 0%, 7%, .1);
  }

  .iy-slug-ipt {
    width: 80%;
  }

  .me-write-info {
    line-height: 60px;
    font-size: 18px;
    font-weight: 600;
  }

  .me-write-btn {
    margin-top: 14px;
    display: flex;
  }

  .me-write-box {
    max-width: 900px;
    margin: 80px auto 0;
  }

  .me-write-main {
    padding: 0;
  }

  .me-write-title {
  }

  .me-write-input textarea {
    font-size: 32px;
    font-weight: 600;
    height: 20px;
    border: none;
  }

  .me-write-editor {
    min-height: 650px !important;
  }

  .me-header-left {
    margin-top: 10px;
  }

  .me-title img {
    max-height: 2.4rem;
    max-width: 100%;
  }

  .item {
    margin: 4px;
  }

  .me-write-toolbar-fixed {
    position: fixed;
    width: 900px !important;
    top: 60px;
  }

  .v-note-op {
    box-shadow: none !important;
  }

  .auto-textarea-input, .auto-textarea-block {
    font-size: 18px !important;
  }

  .el-tag {
    margin-right: 10px;
  }

  .el-tag + .el-tag {
    margin-left: 10px;
  }

  .button-new-tag {
    margin-left: 10px;
    height: 32px;
    line-height: 30px;
    padding-top: 0;
    padding-bottom: 0;
  }

  .input-new-tag {
    /*width: 90px;*/
    width: 60%;
    display: block;
    vertical-align: bottom;
  }

  .el-switch__core:after {
    content: "";
    position: absolute;
    top: 1px;
    left: 1px;
    border-radius: 100%;
    transition: all .3s;
    width: 16px;
    height: 16px;
    background-color: #fff;
  }

  .el-switch.is-checked .el-switch__core:after {
    left: 100%;
    margin-left: -17px;
  }
</style>

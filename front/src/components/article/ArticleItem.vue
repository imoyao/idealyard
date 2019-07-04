<template>
  <el-card class="me-area" :body-style="{ padding: '16px' }">
    <div class="me-article-header">

      <a @click="view(id,identifier)" class="me-article-title">{{title}}</a>
      <!--<el-button v-if="weight > 0" class="me-article-icon" type="text">置顶</el-button>-->
      <span class="me-article-icon" type="text">
        <i class="iconfont icon-pushpin"></i>
      </span>
      <span class="me-pull-right me-article-count">
	    	<i class="iconfont icon-comment"></i>&nbsp;{{commentCounts}}
	    </span>
      <span class="me-pull-right me-article-count">
	    	<i class="iconfont icon-read"></i>&nbsp;{{viewCounts}}
	    </span>
    </div>

    <div class="me-artile-description">
      {{summary}}
    </div>
    <div class="me-article-footer">
	  	<span class="me-article-author">
	    	<i class="iconfont icon-user"></i>&nbsp;{{author.nickname}}
	    </span>

      <i class="iconfont icon-tags"></i>
      <!--# TODO:tags 大于三个时显示异常 ,为空时不应该显示图标-->
      <el-tag v-for="t in tags" :key="t.tagname" size="mini" type="success" class="me-article-flag">{{t.tagname}}</el-tag>
      <span class="me-article-category">
	    	<i class="iconfont icon-folder-open"></i>&nbsp;{{category.categoryname}}
	    </span>
      <span class="me-pull-right me-article-count">
	    	<i class="el-icon-time"></i>&nbsp;{{createDate | format}}
	    </span>

    </div>
  </el-card>
</template>

<script>
  import { formatTime } from "../../utils/time";

  export default {
    name: 'ArticleItem',
    props: {
      id: Number,
      identifier: Number,
      weight: Number,
      title: String,
      commentCounts: Number,
      viewCounts: Number,
      summary: String,
      author: Object,
      tags: Array,
      category: Object,
      createDate: String
    },
    data() {
      return {}
    },
    methods: {
      view(postId,identifier) {
        this.$router.push({path: `/post/${identifier}`,name: 'viewpost', params:{id:postId,identifier:identifier}})
      }
    }
  }
</script>

<style scoped>

  .me-article-header {
    /*padding: 10px 18px;*/
    padding-bottom: 10px;
  }

  .me-article-title {
    font-weight: 600;
  }

  .me-article-icon {
    padding: 3px 3px;
    color:red;
  }

  .me-article-count {
    color: #a6a6a6;
    padding-left: 14px;
    font-size: 13px;
  }

  .me-article-flag {
    margin-left: 1px !important;
    font-size: 13px;
  }

  .me-pull-right {
    float: right;
  }

  .me-artile-description {
    font-size: 13px;
    line-height: 24px;
    margin-bottom: 10px;
  }

  .me-article-author {
    color: #a6a6a6;
    padding-right: 18px;
    font-size: 13px;
  }
  .me-article-category {
    color: #a6a6a6;
    padding-left: 18px;
    font-size: 13px;
  }

  .el-tag {
    margin-left: 6px;
  }

</style>

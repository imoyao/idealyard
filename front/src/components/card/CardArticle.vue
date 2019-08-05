<template>
  <el-card :body-style="{ padding: '8px 18px' }">
    <div slot="header" class="me-category-header">
      <span>{{cardHeader}}</span>
    </div>

    <ul class="me-category-list">
      <li v-for="a in articles" @click="view(a.id,a.identifier,a.slug)" :style="itemStyle" :key="a.id" class="me-category-item"><a>{{a.title}}</a>
      </li>
    </ul>
  </el-card>

</template>

<script>
  export default {
    name: 'CardArticle',
    props: {
      cardHeader: {
        type: String,
        required: true
      },
      articles: {
        type: Array,
        required: true
      },
      itemStyle: Object
    },
    data() {
      return {}
    },
    methods: {
      view(postId,identifier,slug) {
        this.$router.push({path: `/posts/${identifier}/${slug}`, params:{id:postId,identifier:identifier,slug:slug}})
      }
    }
  }
</script>

<style scoped>
  .me-category-header {
    font-weight: 600;
  }

  .me-category-list {
    list-style-type: none;
  }

  .me-category-item {
    padding: 4px;
    font-size: 14px;
    color: #5FB878;
  }

  .me-category-item a:hover {
    text-decoration: underline;
  }
</style>

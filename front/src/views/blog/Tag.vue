<!--https://jsbin.com/tipebihugo/edit?html,console,output-->
<!--https://seregpie.github.io/VueWordCloud/-->
<template>

  <tag-cloud
    class="my-tag"
    :words="words"
    :animation-overlap="3"
    :font-size-ratio="3"
    rotation-unit="deg"
    :rotation="0"
    :spacing="0.618"
    :color="([, weight]) => weight > 20 ? 'rgb(255, 78, 105)': weight > 15 ? 'rgb(49, 165, 13)' : weight > 10 ? 'rgb(255, 208, 119)' : weight > 5 ? 'rgb(58, 158, 234)' : weight === 0 ? '#909399' :'rgb(59, 196, 199)'"
    font-family="Roboto"
  >
    <template  slot-scope="{text, weight, word}">
      <div class="item"  v-if="word[1]>0" style="cursor: pointer;" @click="onWordClick(word[2])">
        {{ text }}
      </div>
      <div v-else>
        {{ text }}
      </div>
    </template>
  </tag-cloud>


</template>

<script>
  import VueWordCloud from 'vuewordcloud'
  import {reqAllTags} from '@/api/tag'
  export default {
    name: 'Tag',
    data() {
      return {
        words:[]
      }
    },
    methods: {
      // 组装列表，每个元素内部依次为[tagName，tagCounts，tagId]
      tagInfo(){
        reqAllTags().then(data => {
          let tagObjs = data.data
          console.log(tagObjs)
          for(let tag in tagObjs){
            let tagItem = []
            tagItem.push(tagObjs[tag].tagname)
            tagItem.push(tagObjs[tag].article_counts)
            tagItem.push(tagObjs[tag].id)
            this.words.push(tagItem)
          }
        }).catch(error => {
          if (error !== 'error') {
            this.$message({type: 'error', message: '标签加载失败', showClose: true})
          }
        })
      },
      onWordClick(tagId) {
        this.$router.push({path: `/tag/${tagId}`})
      }
    },
    mounted () {
      this.tagInfo()
    },
    components: {
      "tag-cloud": VueWordCloud,
    }
  }
</script>

<style scoped>
  .my-tag {
    position: inherit !important;
    width: 68% !important;
    height: 100%;
  }

  .item {
    margin-right: 40px;
    width: 0;
  }
  .item:hover {
    text-decoration:underline;
  }
</style>

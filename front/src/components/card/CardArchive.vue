<template>

  <el-card :body-style="{ padding: '8px 18px' }">
    <div slot="header" class="me-category-header">
      <span>{{cardHeader}}</span>
    </div>

    <ul class="me-category-list">
      <li v-for="(a,index) in archives" @click="view(a.year, a.month)" :key="index" v-show="index<limitShowNum" class="me-category-item"><a>{{`${a.year}年${a.month}月`}}</a>
      </li>
    </ul>
    <el-button @click="showMore" type="text" class="show-all-control"><i class="icon-m-right" :class="showIcon">{{showAllTip}}</i></el-button>
  </el-card>

</template>

<script>
  export default {
    name: "CardArchive",
    props: {
      cardHeader: {
        type: String,
        required: true
      },
      archives: {
        type: Array,
        required: true
      }
    },
    data(){
      return{
        isShow: true,
        showAllTip: '我全都要 😜',
        limitShowNum: 6,
        defalutShowNum: 6,
        showIcon:'el-icon-caret-bottom',
      }
    },
    methods: {
      showMore(){
        let showDataLen = Object.keys(this.archives).length
        this.isShow = !this.isShow
        if (this.isShow) {
          this.limitShowNum = this.defalutShowNum
          this.showAllTip ='我全都要 😜'
          this.showIcon = 'el-icon-caret-bottom'
        }else{
          this.limitShowNum = showDataLen
          this.showAllTip ='一般货色 🙄'
          this.showIcon = 'el-icon-caret-top'
        }
      },
      view(year, month) {
        this.$router.push({path: `/archives/${year}/${month}`})
      }
    },
  }
</script>

<style scoped>

  .me-category-header {
    font-weight: 600;
  }
   .show-all-control {
      border-top: 1px solid #eaeefb;
      height: 44px;
      width: 100%;
      box-sizing: border-box;
      background-color: #fff;
      border-bottom-left-radius: 4px;
      border-bottom-right-radius: 4px;
      text-align: center;
      margin-top: -1px;
      color: #d3dce6;
      cursor: pointer;
      position: relative;
   }
   .show-all-control :hover{
     color:#66b1ff;
   }
   .icon-m-right{
     margin-right:60px;
   }
  .me-category-list {
    list-style-type: none;
  }

  .me-category-item {
    display: inline-block;
    width: 40%;
    padding: 4px;
    font-size: 14px;
    color: #5FB878;
  }

  .me-category-item a:hover {
    text-decoration: underline;
  }

</style>

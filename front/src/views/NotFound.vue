<template>
  <div class="view not-found-view">
    <div class="where-is-panfish">
      <img src="../assets/img/bg.png" class="elem bg">
      <img src="../assets/img/panfish.png" class="elem panfish">
      <img src="../assets/img/sea.png" class="elem sea">
      <img src="../assets/img/spray.png" class="elem spray">
    </div>
    <el-button type="primary" class="index-link" @click="goIndex">回到首页</el-button>
  </div>
</template>

<script>
  export default {
    name: 'NotFound',
    methods:{
      goIndex(){
        this.$router.push('/')
      }
    }
  }
</script>

<style scoped>
  .where-is-panfish {
    position: relative;
    width: 52rem;
    max-width: 70%;
    padding-top: 48%;
  }

  .where-is-panfish .bg {
    width: 77.724%;
    transform: translate(-50%, -50%);
  }

  .where-is-panfish .elem {
    position: absolute;
    top: 35%;
    left: 50%;
  }

  .where-is-panfish .sea {
    width: 99.199%;
    transform: translate(-50%, 75.3%);
    opacity: .7;
  }

  .where-is-panfish .spray {
    width: 40.545%;
    transform: translate(-55%, 162%);
    opacity: .4;
  }

  .where-is-panfish .panfish {
    width: 20.994%;
    transform: translate(-55%, 32%);
    animation:panfish 2s ease-out 0s infinite alternate none running;
  }

  .index-link {
    display: block;
    margin-top: 2rem;
    padding: 1.1rem 2rem;
    font-size: 1.2rem;
    color: #fff;
    /*background-color: #007fff;*/
    border-radius: 5px;
  }

  .not-found-view {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    margin-bottom: 4rem;
  }
</style>

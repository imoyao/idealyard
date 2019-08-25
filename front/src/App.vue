<template>
  <div id="app">
    <router-view/>
    <go-top></go-top>
  </div>
</template>

<script>
  import GoTop from '@/components/gotop/GoTop'

  export default {
    name: 'App',
    components: {GoTop}
  }
</script>

<style>
  * {
    margin: 0;
    padding: 0;
  }

  body {
    background-color: #f5f5f5;
    font-weight: 400;
    font-family: "Helvetica Neue", Helvetica, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "微软雅黑", Arial, sans-serif;
    line-height: 1.5;
  }

  a {
    cursor: pointer;
    text-decoration: none;
    transition: none 86ms ease-out;
  }

  a:hover {
    color: #5FB878;
  }

  .me-area {
    background-color: #fff;
    border-right: none;
    border-bottom: solid 1px #e6e6e6;
    box-shadow: 0 1px 3px rgba(26,26,26,.1);
  }

  /*重要声明或slogan*/
  .slogan-declare {
    color: #e11111;
    display: block;
  }

  .icon-m-right {
    margin-right: 6px;
  }

  .no-enough {
    color: #e11111;
  }

  html {
    height: 100%;
  }

  body {
    min-height: 100%;
  }

  body {
    position: relative;
  }

  .me-pull-right {
    float: right;
  }


  .el-divider {
    background-color: #dcdfe6;
    position: relative;
  }

  .el-divider--horizontal {
    display: block;
    height: 1px;
    width: 100%;
    margin: 24px 0;
  }

  .el-divider--vertical {
    display: inline-block;
    width: 1px;
    height: 1em;
    margin: 0 8px;
    vertical-align: middle;
    position: relative;
  }

  .el-divider__text.is-center {
    left: 50%;
    transform: translateX(-50%) translateY(-50%);
  }
</style>

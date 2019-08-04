<template>
  <main class="main">
    <h1 class="title">友情链接</h1>
    <el-row :gutter="12" class="link-list">
      <template v-for="item in friends">
        <el-col :span="6" class="item">

          <el-card shadow="hover" class="card">
            <el-link :underline="false" href="https://www.baidu.com" class="link" target="_blank" style="width:100%;">
              <div class="logo"
                   style="background-image:url(https://subsite-cdn.xitu.io/2018/8/13/16533039b9a9fc09?imageslim) ">
              </div>
              <div class="item-content">
                <el-tooltip effect="light" placement="right">
                  <div class="name" slot="content">吃葡萄不吐葡萄皮<br/>第二行信息</div>
                  <span class="link-title">{{ item }}</span>
                </el-tooltip>
              </div>

            </el-link>

          </el-card>
        </el-col>
      </template>
    </el-row>
  </main>

</template>

<script>
  export default {
    name: 'Link',
    data() {
      return {
        friends: ['a', '趴在窗口看书的人', 'cccccccccccccc', 'dddddddddd', 'eeeeeeeeeeee', 'aaaaaaaaaaa', 'bbbbbbbbbbbb', 'cccccccccccccc', 'ddddd', 'eeeeeeeeeeee']
      }
    }
  }
</script>

<style scoped>
  .main {
    -ms-flex: 1 1 auto;
    flex: 1 1 auto;
    margin: 0 auto;
    max-width: 980px;
    display: block;
  }

  .main .title {
    margin: 60px 0 30px 0;
    font-size: 32px;
    font-weight: 100;
    text-align: center;
    color: #000;
  }

  h1 {
    margin: .67em 0;
    display: block;
    font-size: 2em;
    margin-block-start: 0.67em;
    margin-block-end: 0.67em;
    margin-inline-start: 0px;
    margin-inline-end: 0px;
    font-weight: bold;
  }

  ul {
    padding: 0;
    margin: 0;
    display: block;
    list-style-type: disc;
    margin-block-start: 1em;
    margin-block-end: 1em;
    margin-inline-start: 0px;
    margin-inline-end: 0px;
    padding-inline-start: 40px;
  }

  .main .link-list {
    margin: 30px auto 60px auto;
    padding: 0;
    line-height: 0;
    list-style: none;
  }

  .item-content {
    /*padding: 14px;*/
    /*line-hight:14px;*/
    width: 100%;
    text-align: center;
    word-wrap: break-word;
    word-break: break-all;
    overflow: hidden
  }

  /*.main .link-list .item {*/
  /*display: inline-block;*/
  /*position: relative;*/
  /*margin: 0 8px 16px 8px;*/
  /*width: 180px;*/
  /*height: 74px;*/
  /*background-color: #fff;*/
  /*box-shadow: inset 0 0 0 1px #f1f1f1;*/
  /*overflow: hidden;*/
  /*box-sizing: border-box;*/
  /*}*/

  li {
    text-align: -webkit-match-parent;
    list-style: none;
    display: list-item;
  }

  .main .link-list .item .link .name {
    padding: 0 5px;
    width: 0;
    height: 0;
    font-size: 14px;
    line-height: 1.5;
    color: #333;
    opacity: 0;
  }
  /*TODO: 居中显示异常*/
  .main .link-list .item .link .logo {
    padding-left: 30px;
    height: 30px;
    width: 70%;
    background-position: center;
    background-repeat: no-repeat;
    background-size: contain;
  }

  .main .link-list .item .link {
    display: -ms-flexbox;
    display: flex;
    -ms-flex-align: center;
    align-items: center;
    -ms-flex-pack: center;
    justify-content: center;
    height: 100%;
    text-decoration: none;
  }

  .link-title {
    width: 120px;
    line-height: 14px;
    outline: none;
  }

  a {
    text-decoration: none;
    cursor: pointer;
    color: #909090;
    background-color: transparent;
  }

  a:-webkit-any-link {
    color: -webkit-link;
    cursor: pointer;
    text-decoration: underline;
  }

  .right {
    float: right;
    width: 60px;
  }

  .el-link {
    display: inline-flex;
    flex-direction: row;
    align-items: center;
    justify-content: center;
    vertical-align: middle;
    position: relative;
    text-decoration: none;
    outline: none;
    cursor: pointer;
    padding: 0;
    font-size: 14px;
    font-weight: 500;
  }

  .el-link.el-link--default {
    color: #606266;
  }

  .el-card {
    border-radius: 4px;
    border: 1px solid #ebeef5;
    background-color: #fff;
    overflow: hidden;
    color: #303133;
    transition: .3s;
  }

  .el-card__body {
    padding: 20px;
  }

  .el-card.is-always-shadow, .el-card.is-hover-shadow:focus, .el-card.is-hover-shadow:hover {
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, .1);
  }

  .card:hover {
    box-shadow: 0 0 8px 0 rgba(232, 237, 250, .6), 0 2px 4px 0 rgba(232, 237, 250, .5)
  }
</style>

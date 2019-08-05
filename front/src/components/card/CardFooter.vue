<template>
  <el-card class="more-section">
    <section>
      <div class="more-list">
        <router-link class="item" to="/about">关于</router-link>
        <el-divider direction="vertical"></el-divider>
        <router-link class="item" to="/links">友情链接</router-link>
        <el-divider direction="vertical"></el-divider>
        <el-link class="item" href="https://support.qq.com/products/67072" target="_blank">吐槽</el-link>
      </div>

      <ul class="more-list">
        <li class="item"><span>©2019 别院牧志</span></li>
      </ul>
      <ul class="more-list">
        <li class="item">
          <p>Powered by
            <strong>
              <span class="me-login-design-color">iMOYAO</span>
            </strong>
          </p>

        </li>
      </ul>
      <ul class="more-list">
        <li class="item"><span>就命运而言，休论公道。</span></li>
      </ul>
      <ul class="more-list">
        <li class="item"><a name="beianLink" href="http://beian.miit.gov.cn"
                            target="_blank">京ICP备666xxx666号</a></li>
      </ul>
    </section>
  </el-card>
</template>

<script>
  export default {
    name: 'CardFooter',
    methods: {}
  }
</script>

<style scoped>
  .more-section {
    background-color: transparent;
    text-align: center;
    color: #909090;
    font-size: 1.1rem;
    box-shadow: none;
    border: 0;
  }

  .el-divider--vertical {
    display: inline-block;
    width: 1px;
    height: 1em;
    margin: 0 8px;
    vertical-align: middle;
    position: relative;
  }

  .el-divider {
    background-color: #dcdfe6;
    position: relative;
  }

  .more-section .more-list {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-bottom: .4rem;
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

  .more-section .more-list .item:not(:last-child)::after {
    /*content: "·";*/
    margin: 0 0.4rem;
  }

  .me-login-design-color {
    color: #5FB878 !important;
  }

  a {
    background-color: transparent;
    text-decoration: none !important;
    cursor: pointer !important;
    color: #909090 !important;
  }

  a:hover {
    color: #66b1ff !important;
  }

  a:-webkit-any-link {
    color: -webkit-link;
    cursor: pointer;
    text-decoration: underline;
  }

  li {
    list-style: none;
    display: inline-block;
    text-align: -webkit-match-parent;
  }

  .more-section {
    background-color: transparent;
    text-align: center;
    color: #909090;
    font-size: 14px;
    box-shadow: none;
  }
</style>

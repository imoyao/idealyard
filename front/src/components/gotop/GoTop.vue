<template>
  <!--<transition name="el-zoom-in-center">-->
  <div>
    <transition-group>
      <div v-bind:key="1" @click="toTop" v-show="topShow" class="float-btn me-to-top"><i class="iconfont icon-arrowup"></i></div>
      <div v-bind:key="2" v-show="feedback" class="float-btn me-feed-back">
        <a href="https://support.qq.com/product/67072" target="_blank">
          <i class="iconfont icon-message"></i>
        </a>
      </div>
    </transition-group>
  </div>
</template>

<script>
  export default {
    name: 'GoTop',
    data() {
      return {
        topShow: false,
        feedback: true,
      }
    },
    methods: {
      toTop() {
        document.body.scrollTop = 0;
        document.documentElement.scrollTop = 0;
        this.topShow = false;
      },
      needToTop() {
        let curHeight = document.documentElement.scrollTop || document.body.scrollTop;

        if (curHeight > 400) {
          this.topShow = true;
        } else {
          this.topShow = false;
        }

      }
    },
    mounted() {
      /**
       * 等到整个视图都渲染完毕
       */
      this.$nextTick(function () {
        window.addEventListener('scroll', this.needToTop);
      });
    }
  }
</script>

<style scoped>
  .float-btn {
    background-color: #fff;
    position: fixed;
    right: 100px;
    width: 40px;
    height: 40px;
    border-radius: 20px;
    cursor: pointer;
    transition: .3s;
    box-shadow: 0 0 6px rgba(0, 0, 0, .12);
    z-index: 5;
  }

  .me-to-top {
    bottom: 150px;
  }

  .me-feed-back {
    bottom: 90px;
  }

  .me-feed-back i {
    color: #00d1b2;
    display: block;
    line-height: 40px;
    text-align: center;
    font-size: 20px;
  }

  .me-to-top i {
    color: #00d1b2;
    display: block;
    line-height: 40px;
    text-align: center;
    font-size: 20px;
  }

</style>

<!--该页面仿照知乎个人信息编辑页-->
<template>
  <div id="profile">
    <div id="db-nav-sns" class="nav">
      <div class="nav-wrap">
        <div class="nav-primary">
          <el-header>
            <el-menu style="background: transparent">
              <router-link to="/" class="me-title">
                <img src="../assets/img/logo.png" alt="别院牧志">
                <h1 class="site-name">别院牧志</h1>
              </router-link>
            </el-menu>
          </el-header>
        </div>
      </div>
    </div>

    <div class="profile-wrap">
      <div class="profile-main">
        <div class="block">
          <el-upload
            class="upload-bg-btn"
            action="https://jsonplaceholder.typicode.com/posts/"
            :on-preview="handlePreview"
            :on-remove="handleRemove"
            :before-remove="beforeRemove"
            multiple
            :limit="3"
            :show-file-list=false
            :on-exceed="handleExceed"
            :file-list="fileList">
            <el-button size="small" type="primary" class="profile-bg-btn" @click="updateProfileBG">编辑封面图片</el-button>
            <!--<el-button size="small" type="primary">点击上传</el-button>-->
            <!--<div slot="tip" class="el-upload__tip">只能上传jpg/png文件，且不超过500kb</div>-->
          </el-upload>
          <el-image :src="src">
            <div slot="error" class="image-slot">
              <i class="el-icon-picture-outline"></i>
            </div>
            <div slot="placeholder" class="image-slot">
              加载中<span class="dot">...</span>
            </div>
          </el-image>
        </div>

        <div>
          <div class="ProfileHeader-contentHead">
            <h1 class="ProfileHeader-title">
              <div class="FullnameField-editable"><span class="FullnameField-name">{{userProfileForm.username}}</span>
                <button type="button" class="Button ModifyButton Field-modify Field-modify-hidden Button--link">
                  修改
                </button>
              </div>
            </h1>
            <div class="ProfileHeader-expandActions ProfileEdit-expandActions">
              <a href="/">返回主页</a></div>
          </div>
          <el-form ref="userProfileForm" :model="userProfileForm" label-width="80px">
            <el-form-item label="Slogan" @mouseenter.native="showEditSlogan()" @mouseleave.native="hideEditSlogan()">
              <div>
                <span v-show="!sloganSpan2Ipt">
                  {{ userProfileForm.slogan }}
                </span>
                <el-link class="field-modify edit" v-show="showSloganBtn && !sloganSpan2Ipt" @click="editSlogan"
                         type="primary">编辑
                </el-link>
              </div>

              <el-link class="field-modify cancel" v-show="sloganSpan2Ipt" @click="cancelEditSlogan" type="info">取消
              </el-link>
              <el-link class="field-modify save" v-show="sloganSpan2Ipt" @click="saveSlogan" type="info">保存</el-link>
              <el-input class="profile-ipt" v-show="sloganSpan2Ipt" v-model="userProfileForm.slogan"></el-input>

            </el-form-item>

            <el-form-item label="居住地" @mouseenter.native="showEditLocation()" @mouseleave.native="hideEditLocation()">
              <div>
                <span v-show="!locationSpan2Ipt">
                  {{ userProfileForm.location }}
                </span>
                <el-link class="field-modify edit" v-show="showLocationBtn && !locationSpan2Ipt" @click="editLocation"
                         type="primary">编辑
                </el-link>
              </div>

              <el-link class="field-modify cancel" v-show="locationSpan2Ipt" @click="cancelEditLocation" type="info">取消
              </el-link>
              <el-link class="field-modify save" v-show="locationSpan2Ipt" @click="saveLocation" type="info">保存
              </el-link>
              <el-input class="profile-ipt" v-show="locationSpan2Ipt" v-model="userProfileForm.location"></el-input>
            </el-form-item>

            <el-form-item label="昵称" @mouseenter.native="showEditNickname()" @mouseleave.native="hideEditNickname()">
              <div>
                <span v-show="!nicknameSpan2Ipt">
                  {{ userProfileForm.nickname }}
                </span>
                <el-link class="field-modify edit" v-show="showNicknameBtn && !nicknameSpan2Ipt" @click="editNickname"
                         type="primary">编辑
                </el-link>
              </div>

              <el-link class="field-modify cancel" v-show="nicknameSpan2Ipt" @click="cancelEditNickname" type="info">取消
              </el-link>
              <el-link class="field-modify save" v-show="nicknameSpan2Ipt" @click="saveNickname" type="info">保存
              </el-link>
              <el-input class="profile-ipt" v-show="nicknameSpan2Ipt" v-model="userProfileForm.nickname"></el-input>
            </el-form-item>
            <el-form-item label="用户名" @mouseenter.native="showEditUsername()" @mouseleave.native="hideEditUsername()">
              <div>
                <span v-show="!usernameSpan2Ipt">
                  {{ userProfileForm.username }}
                </span>
                <el-link class="field-modify edit" v-show="showUsernameBtn && !usernameSpan2Ipt" @click="editUsername"
                         type="primary">编辑
                </el-link>
              </div>

              <el-link class="field-modify cancel" v-show="usernameSpan2Ipt" @click="cancelEditUsername" type="info">取消
              </el-link>
              <el-link class="field-modify save" v-show="usernameSpan2Ipt" @click="saveUsername" type="info">保存
              </el-link>
              <el-input class="profile-ipt" v-show="usernameSpan2Ipt" v-model="userProfileForm.username"></el-input>
            </el-form-item>
            <el-form-item label="注册邮箱" @mouseenter.native="showEditEmail()" @mouseleave.native="hideEditEmail()">
              <div>
                <span v-show="!emailSpan2Ipt">
                  {{ userProfileForm.email }}
                </span>
                <el-link class="field-modify edit" v-show="showEmailBtn && !emailSpan2Ipt" @click="editEmail"
                         type="primary">编辑
                </el-link>
              </div>

              <el-link class="field-modify cancel" v-show="emailSpan2Ipt" @click="cancelEditEmail" type="info">取消
              </el-link>
              <el-link class="field-modify save" v-show="emailSpan2Ipt" @click="saveEmail" type="info">保存</el-link>
              <el-input class="profile-ipt" v-show="emailSpan2Ipt" v-model="userProfileForm.email"></el-input>
            </el-form-item>

            <el-form-item v-show="sloganSpan2Ipt||locationSpan2Ipt||nicknameSpan2Ipt||usernameSpan2Ipt||emailSpan2Ipt">
              <el-button type="primary" @click="onSubmit">更新信息</el-button>
              <el-button
                         @click="onCancel">取消
              </el-button>
            </el-form-item>
          </el-form>
        </div>

      </div>
    </div>
  </div>

</template>

<script>
  export default {
    name: 'Profile',
    data() {
      return {
        showSloganBtn: false,
        sloganSpan2Ipt: false,
        showLocationBtn: false,
        locationSpan2Ipt: false,
        showNicknameBtn: false,
        nicknameSpan2Ipt: false,
        showUsernameBtn: false,
        usernameSpan2Ipt: false,
        showEmailBtn: false,
        emailSpan2Ipt: false,
        src: 'https://pic2.zhimg.com/80/v2-e407aeb66333b4b8e1b4bbfc3b2d4d5d_r.jpg',
        userProfileForm: {
          slogan: '而今笑问君何在？醉看鱼肚白。',
          location: '北京',
          nickname: 'imoyao',
          username: '张牧志',
          email: 'imsantu@126.com',
          avatar: 'beijing',
        },
        fileList: [{name: 'zhimg', url: 'https://pic2.zhimg.com/80/v2-e407aeb66333b4b8e1b4bbfc3b2d4d5d_r.jpg'}]
      }
    },
    methods: {
      onSubmit() {
        console.log('submit!');
      },
      onCancel() {
        this.sloganSpan2Ipt = false
        this.locationSpan2Ipt = false
        this.nicknameSpan2Ipt = false
        this.usernameSpan2Ipt = false
        this.emailSpan2Ipt = false
      },
      updateProfileBG() {
        console.log('update success-------------')
      },
      handleRemove(file, fileList) {
        console.log(file, fileList);
      },
      handlePreview(file) {
        console.log(file);
      },
      handleExceed(files, fileList) {
        this.$message.warning(`当前限制选择 3 个文件，本次选择了 ${files.length} 个文件，共选择了 ${files.length + fileList.length} 个文件`);
      },
      beforeRemove(file, fileList) {
        return this.$confirm(`确定移除 ${file.name}？`);
      },
      // slogan
      showEditSlogan() {
        this.showSloganBtn = true
      },
      hideEditSlogan() {
        this.showSloganBtn = false
      },
      editSlogan() {
        this.sloganSpan2Ipt = true
      },
      cancelEditSlogan() {
        this.sloganSpan2Ipt = false
      },
      saveSlogan() {
        console.log('保存到后端还没写')
        this.sloganSpan2Ipt = false
      },
      // location
      showEditLocation() {
        this.showLocationBtn = true

      },
      hideEditLocation() {
        this.showLocationBtn = false
      },
      editLocation() {
        this.locationSpan2Ipt = true
      },
      cancelEditLocation() {
        this.locationSpan2Ipt = false
      },
      saveLocation() {
        console.log('保存到后端还没写')
        this.locationSpan2Ipt = false
      },
      // nickname
      showEditNickname() {
        this.showNicknameBtn = true
      },
      hideEditNickname() {
        this.showNicknameBtn = false
      },
      editNickname() {
        this.nicknameSpan2Ipt = true
      },
      cancelEditNickname() {
        this.nicknameSpan2Ipt = false
      },
      saveNickname() {
        console.log('保存到后端还没写')
        this.nicknameSpan2Ipt = false
      },
      // username
      showEditUsername() {
        this.showUsernameBtn = true

      },
      hideEditUsername() {
        this.showUsernameBtn = false

      },
      editUsername() {
        this.usernameSpan2Ipt = true
      },
      cancelEditUsername() {
        this.usernameSpan2Ipt = false
      },
      saveUsername() {
        console.log('保存到后端还没写')
        this.usernameSpan2Ipt = false
      },
      // email
      showEditEmail() {
        this.showEmailBtn = true

      },
      hideEditEmail() {
        this.showEmailBtn = false

      },
      editEmail() {
        this.emailSpan2Ipt = true
      },
      cancelEditEmail() {
        this.emailSpan2Ipt = false
      },
      saveEmail() {
        this.emailSpan2Ipt = false
      },
    }
  }
</script>

<style scoped>
  #db-nav-sns {
    position: relative;
    zoom: 1;
    background: #edf4ed;
  }

  #db-nav-sns .nav-primary {
    width: 100%;
    height: 60px;
    margin: 0 auto;
    overflow: hidden;
    padding: 22px 0 20px;
    zoom: 1;
  }

  .site-name {
    display: inline-block;
    font-size: 1em;
    color: #5FB878
  }

  .me-title {
    margin-top: 10px;
    font-size: 24px;
  }

  .me-title img {
    max-height: 2.4rem;
    max-width: 100%;
  }

  .profile-wrap {
    width: 1040px;
    height: 900px;
    margin: 20px auto 0;
    overflow: hidden;
  }

  .profile-main {
    float: left;
    width: 590px;
  }

  .block {
    width: 1200px;
    height: 400px;
  }
  .profile-content{
    width: 900px;
  }
  .profile-bg-btn {
    float: right;
    position: absolute;
    background: transparent;
    /*top: 24px;*/
    /*right: 24px;*/
    z-index: 2;
  }

  .upload-bg-btn {
    height: 0px;
    margin-left: 15px;
  }

  .field-modify {
    float: right;
    margin-left: 16px;
    line-height: inherit;
    color: #409EFF;
    -webkit-transition: opacity .1s;
    transition: opacity .1s;
  }

  .edit:hover {
    color: #67c23a;
  }

  .save:hover {
    color: #409EFF;
  }

  .cancel:hover {
    color: #909399;
  }

  .profile-ipt {
    width: 60%;
  }

  .demonstration {
    display: block;
    color: #8492a6;
    font-size: 14px;
    margin-bottom: 20px;
  }

  .ProfileEdit {
    width: 1000px;
    padding: 0 16px;
    margin: 14px auto;
    font-size: 15px;
    color: #1a1a1a;
  }

  .UserCoverEditor {
    position: relative;
  }

  .UserCover {
    position: relative;
    height: 240px;
    overflow: hidden;
    background: #f6f6f6;
    border-top-right-radius: 1px;
    border-top-left-radius: 1px;
    -webkit-transition: height .3s;
    transition: height .3s;
  }

  .UserCover-image, .UserCover-image img {
    width: 100%;
    height: 100%;
    -o-object-fit: cover;
    object-fit: cover;
  }

  .UserCover-image {
    -webkit-transition: -webkit-transform 6s ease-out;
    transition: -webkit-transform 6s ease-out;
    transition: transform 6s ease-out;
    transition: transform 6s ease-out, -webkit-transform 6s ease-out;
  }
</style>

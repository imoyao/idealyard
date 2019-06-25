<template>
  <div id="login">
    <Row type="flex" justify="center">
      <!--<img src="../assets/login.jpg" alt="" :style="bg">-->
      <Col span="5">
        <Card class="form">
          <div slot="title">
            登录页
          </div>
          <Form ref="formInline" :model="formInline" :rules="ruleInline">
            <FormItem prop="username">
              <Input type="text" v-model="formInline.username" placeholder="用户名" size="large"
                     @on-enter="handleSubmit('formInline', formInline)">
              <Icon slot="prepend" type="person"></Icon>
              </Input>
            </FormItem>
            <FormItem prop="password">
              <Input type="password" v-model="formInline.password" placeholder="密码" size="large"
                     @on-enter="handleSubmit('formInline', formInline)">
              <Icon slot="prepend" type="locked"></Icon>
              </Input>
            </FormItem>
            <FormItem>
              <Button type="info" @click="handleSubmit('formInline', formInline)" long>登录</Button>
            </FormItem>
          </Form>
        </Card>
      </Col>
    </Row>
  </div>
</template>
<script>
  export default {
    name: 'Login',
    data() {
      return {
        formInline: {
          username: '',
          password: ''
        },
        ruleInline: {
          username: [
            {required: true, message: '请填写用户名', trigger: 'blur'}
          ],
          password: [
            {required: true, message: '请填写密码', trigger: 'blur'},
            {type: 'string', min: 6, message: '密码长度不能小于6位', trigger: 'blur'}
          ]
        },
        bg: {
          width: `${window.innerWidth}px`,
          height: `${window.innerHeight}px`,
          position: "absolute",
        }
      }
    },
    methods: {
      handleSubmit(name, form) {
        this.$refs[name].validate((valid) => {
          if (valid) {
            this.$axios.defaults.auth = {
              username: form.username,
              password: form.password,
            }
            this.$axios.get('/api/login').then(response => {
              this.$Message.success("提交成功")
              let data = response.data
              this.$store.commit('setToken', data)
              this.$router.push('/')
            }).catch(error => {
              this.$Message.error(error.status)
            })
          } else {
            this.$Message.error('表单验证失败!');
          }
        })
      }
    }
  }
</script>

<style scoped>

  .form {
    text-align: center;
    margin-top: 150px;

  }

  p {
    font-size: 30px;
  }
</style>

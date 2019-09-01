import Vuex from 'vuex'
import Vue from 'vue'
import {getToken, setToken, removeToken} from '@/request/token'
import {requestLogin, reqUserInfo, logout, register} from '@/api/login'

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    id: '',
    account: '',
    name: '',
    avatar: '',
    token: getToken(),
  },
  mutations: {
    SET_TOKEN: (state, token) => {
      state.token = token;
    },
    SET_ACCOUNT: (state, account) => {
      state.account = account
    },
    SET_NAME: (state, name) => {
      state.name = name
    },
    SET_AVATAR: (state, avatar) => {
      state.avatar = avatar
    },
    SET_ID: (state, id) => {
      state.id = id
    },
    SET_CONFIRM: (state, confirmed) => {
      state.confirmed = confirmed
    }
  },
  // 异步操作
  actions: {
    login({commit}, user) {
      return new Promise((resolve, reject) => {
        requestLogin(user.account, user.password).then(data => {
          commit('SET_TOKEN', data.data['token'])
          setToken(data.data['token'])
          resolve()
        }).catch(error => {
          console.log('err in store', error)
          reject(error)
        })
      })
    },
    // 获取用户信息
    getUserInfo({commit, state}) {
      let that = this
      return new Promise((resolve, reject) => {
        reqUserInfo().then(data => {
          if (data.data) {
            // TODO:此处需要整理或者更好处理
            let account = data.data.account || data.data.nickname
            commit('SET_ACCOUNT', account)
            commit('SET_NAME', data.data.nickname)
            commit('SET_AVATAR', data.data.avatar)
            commit('SET_ID', data.data.id)
            commit('SET_CONFIRM', data.data.confirmed)
          } else {
            commit('SET_ACCOUNT', '')
            commit('SET_NAME', '')
            commit('SET_AVATAR', '')
            commit('SET_ID', '')
            commit('SET_CONFIRM', '')
            removeToken()
          }
          resolve(data)
        }).catch(error => {
          reject(error)
        })
      })
    },
    // 退出
    logout({commit, state}) {
      return new Promise((resolve, reject) => {
        logout().then(data => {
          commit('SET_TOKEN', '')
          commit('SET_ACCOUNT', '')
          commit('SET_NAME', '')
          commit('SET_AVATAR', '')
          commit('SET_ID', '')
          removeToken()
          resolve()

        }).catch(error => {
          reject(error)
        })
      })
    },
    // 前端 登出
    fedLogOut({commit}) {
      return new Promise(resolve => {
        commit('SET_TOKEN', '')
        commit('SET_ACCOUNT', '')
        commit('SET_NAME', '')
        commit('SET_AVATAR', '')
        commit('SET_ID', '')
        removeToken()
        resolve()
      }).catch(error => {
        reject(error)
      })
    },
    register({commit}, user) {
      return new Promise((resolve, reject) => {
        register(user).then((data) => {
          // TODO:此处是否设置token?
          commit('SET_TOKEN', data.data['token'])
          setToken(data.data['token'])
          resolve()
        }).catch((error) => {
          reject(error)
        })
      })
    }
  }
})

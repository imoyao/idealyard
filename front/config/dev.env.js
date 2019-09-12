'use strict'
const merge = require('webpack-merge')
const prodEnv = require('./prod.env')

module.exports = merge(prodEnv, {
  NODE_ENV: '"development"',
  // BASE_API: '"http://localhost:8888/"'
  BASE_API: '"http://192.168.116.21:5000/api"'
  // BASE_API: '"http://192.168.31.133:5000/api"'
})

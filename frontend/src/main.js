import Vue from 'vue'
import App from './App.vue'
import router from './router'
import './plugins/element.js'
// import './utils/mock.js'
import global from './utils/Global'

import axios from 'axios'

axios.defaults.withCredentials = true;
axios.defaults.baseURL = 'http://127.0.0.1:8000/api';
axios.defaults.xsrfCookieName = 'token'; // default
axios.defaults.xsrfHeaderName = 'Authorization'; // default


Vue.config.productionTip = false
Vue.prototype.GLOBAL = global

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')

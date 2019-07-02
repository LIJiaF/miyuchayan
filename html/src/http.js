import axios from 'axios'
import router from './router/router'

// 超时时间
axios.defaults.timeout = 5000;

axios.interceptors.response.use(
  response => {
    return response;
  },
  error => {
    if (error.response) {
      switch (error.response.status) {
        case 401:
          sessionStorage.removeItem('username');
          router.replace({
            path: 'login',
            query: {redirect: router.currentRoute.fullPath}
          })
      }
    }
    return Promise.reject(error.response.data);   // 返回接口返回的错误信息
  });

export default axios;

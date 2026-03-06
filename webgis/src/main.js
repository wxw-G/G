import { createApp } from 'vue';  // 使用 Vue 3 的 createApp 方法
import App from './App.vue';

import router from './router';
import ElementPlus from 'element-plus';  // 导入 Element Plus
import 'element-plus/dist/index.css';    // 导入 Element Plus 的样式文件
//import axios from 'axios';               // 导入 Axios

const app = createApp(App);  // 创建 Vue 应用实例


// 配置 Axios
// 修改后的axios配置
//app.config.globalProperties.$http = axios.create({
 //   baseURL: '/api', // 使用代理路径
   // timeout: 5000
//});
app.use(router);             // 使用路由
app.use(ElementPlus);        // 使用 Element Plus

app.mount('#app');           // 挂载应用


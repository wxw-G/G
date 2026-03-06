import { createRouter, createWebHistory } from 'vue-router';
import UserLogin from '../views/UserLogin.vue'; // 导入登录页面
import UserRegister from '../views/UserRegister.vue'; // 导入注册页面
import OpenlayersMap from '../views/OpenlayersMap.vue';
import DisasterList from '../views/DisasterList.vue';
import DisasterAnalysis from '../views/DisasterAnalysis.vue';
import ShelterList from '../views/ShelterList.vue'; // 导入避难所列表页面

const routes = [
  {
    path: '/',
    name: 'UserLogin',
    component: UserLogin,
  },
  {
    path: '/register',
    name: 'UserRegister',
    component: UserRegister,
  },
  {
    path: '/map',
    name: 'OpenlayersMap',
    component: OpenlayersMap,
  },
  {
    path: '/disaster-list',
    name: 'DisasterList',
    component: DisasterList,
  },
  {
    path: '/analysis',
    name: 'StatisticalAnalysis',
    component: DisasterAnalysis,
  },
  {
    path: '/shelter',
    name: 'ShelterList',
    component: ShelterList, // 使用导入的组件
  },
  // 其他路由配置...
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
import Vue from 'vue';
import Router from 'vue-router';
import crud from '../components/crud.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'crud',
      component: crud,
    },
  ],
});

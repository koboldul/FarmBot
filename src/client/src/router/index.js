import Vue from 'vue';
import Router from 'vue-router';
import CmdsDash from '@/components/CmdsDash';
import Schedule from '@/components/Schedule';


Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/Schedule',
      name: 'Schedule',
      component: Schedule,
    },
    {
      path: '/',
      name: 'CmdDash',
      component: CmdsDash,
    },
  ],
  mode: 'hash',
});

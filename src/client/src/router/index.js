import { createRouter, createWebHashHistory } from 'vue-router';
import CmdsDash from '@/components/CmdsDash.vue';
import Schedule from '@/components/Schedule.vue';

export default createRouter({
  history: createWebHashHistory(),
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
});

import { createWebHistory, createRouter } from "vue-router";

import LogIn from '../pages/Log-in.vue';
import SignUp from '../pages/Sing-up.vue';
import RecoveryPassword from '../pages/RecoveryPassword.vue';
import Home from '../pages/Home.vue';

const routes =  [
  { path: '/', name: 'LogIn', component: LogIn },
    { path: '/signup', name: 'SignUp', component: SignUp },
    { path: '/recovery-password', name: 'RecoveryPassword', component: RecoveryPassword },
  { path: '/home', name: 'Home', component: Home }
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes: routes,
  linkActiveClass: 'active'
})

export default router;

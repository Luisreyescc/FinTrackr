import { createWebHistory, createRouter } from "vue-router";

import LogIn from '../pages/Log-in.vue';
import SignUp from '../pages/Sign-up.vue';
import RecoveryPassword from '../pages/RecoveryPassword.vue';
import Home from '../pages/Home.vue';
import Status from '../pages/Status.vue';
import History from '../pages/History.vue';
import Leaderboard from '../pages/Leaderboard.vue';

const routes =  [
  { path: '/', name: 'LogIn', component: LogIn },
  { path: '/signup', name: 'SignUp', component: SignUp },
  { path: '/recovery-password', name: 'RecoveryPassword', component: RecoveryPassword },
  { path: '/home', name: 'Home', component: Home },
  { path: '/status', name: 'Status', component: Status },
  { path: '/history', name: 'History', component: History },
  { path: '/leaderboard', name: 'Leaderboard', component: Leaderboard }
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes: routes,
})

export default router;

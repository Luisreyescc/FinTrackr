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

// Global navigation guard
router.beforeEach((to, from, next) => {
  const isLoggedIn = !!sessionStorage.getItem("isLoggedIn");

  // Public routes that don't require authentication
  const publicPages = ['/', '/signup', '/recovery-password'];
  const isPublicPage = publicPages.includes(to.path);

  // If not logged in and trying to access a protected page, redirect to login
  if (!isLoggedIn && !isPublicPage) {
    return next('/');
  }

  // If logged in and trying to access a public page, redirect to home
  if (isLoggedIn && isPublicPage) {
    return next('/home');
  }

  // If all checks pass, proceed to the requested route
  next();
});

export default router;

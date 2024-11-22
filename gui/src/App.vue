<template>
  <div id="app">
    <AppHeader v-if="showBanner" :isLoggedIn="isLoggedIn" @logout="logout"/>
    <div class="main-content scrollbar">
      <router-view @login="login"/>
    </div>
  </div>
</template>
 
<script>
import AppHeader from '@/components/header.vue';
import '@/css/scrollbar.css';
 
export default {
  name: 'App',
  components: {
    AppHeader
  },
  data() {
    return {
      isLoggedIn: !!sessionStorage.getItem("isLoggedIn") // Check session storage for login status
    };
  },
  computed: {
    showBanner() {
      const bannerRoutes = ['/home', '/status', '/history', '/leaderboard', '/edit-profile'];
      return bannerRoutes.includes(this.$route.path);
    }
  },
  methods: {
    login() {
      this.isLoggedIn = true;
      sessionStorage.setItem("isLoggedIn", "true"); // Store login state in session
      this.$router.push('/home'); // Redirect to Home page by default after login
    },
    logout() {
      this.isLoggedIn = false;
      sessionStorage.removeItem("isLoggedIn"); // Remove login state from session
      this.$router.push('/'); // Redirect to Log-in page after sign-out
    }
  },
  watch: {
    isLoggedIn(newValue) {
      // Sync the header's login status when it changes
      sessionStorage.setItem("isLoggedIn", newValue ? "true" : "false");
    }
  }
};
</script>

<style>
html, body {
    height: 100%;
    width: 100%;
    margin: 0;
    padding: 0;
    overflow: auto;
}

#app {
    font-family: "Wix Madefor Display", sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    overflow: auto;
    color: #2c3e50;
}
</style>

<template>
  <div id="app">
    <AppHeader :isLoggedIn="isLoggedIn" @logout="logout"/>
    <div class="main-content">
      <router-view @login="login"/>
    </div>
  </div>
</template>
 
<script>
import AppHeader from './components/header.vue';
 
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
  #app {
  font-family: "Wix Madefor Display", sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  }
</style>

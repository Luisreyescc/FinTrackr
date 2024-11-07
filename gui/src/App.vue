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
      isLoggedIn: false // Update later
    };
  },
  methods: {
    login() {
      this.isLoggedIn = true;
      this.$router.push('/home'); // Redirect to Home page by default after login
    },
    logout() {
      this.isLoggedIn = false;
      this.$router.push('/'); // Redirect to Log-in page after sign-out
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

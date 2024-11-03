<template>
  <div class="login-page">
    <!-- Profile Icon -->
    <img src="@/assets/profile_picture.png" alt="Profile Icon" class="profile-icon" />
    <!-- Login Form -->
    <login-form @login="login" @goToSignUp="goToSignUp" @goToRecovery="goToRecovery"/>
  </div>
</template>

<script>
import LoginForm from '../components/login-form.vue';
import axios from 'axios';
  
export default {
  name: 'LogIn',
  components: {
    LoginForm
  },
  methods: {
   async login({ username, password }) {
   // Temporary login logic for now
   if (username && password) {
     try {
       const response = await axios.post('https://here_goes_the_backend_url/signup', {
         username,
         password
       });
       if (response.status === 200) {
         this.$router.push('/home');
       }
     } catch (error) {
       console.error('Login failed:', error);
       alert('Invalid username or password. Please try again.');
     }
   } else {
     alert('Please enter username and password');
   }
   },
    goToSignUp() {
      this.$router.push('/signup');
    },
    goToRecovery() {
      // Navigate to the recovery password page
      this.$router.push('/recovery-password');
    }
  }
};
</script>

<style scoped>
/* Center the login page */
.login-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  font-family: Arial, sans-serif;
}

/* Profile icon styling */
.profile-icon {
  width: 100px;
  height: 100px;
  margin-bottom: 20px;
  border-radius: 50%;
  border: 2px solid #ccc;
}
</style>

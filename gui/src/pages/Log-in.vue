<template>
  <div class="login-page">
    <!-- Profile Icon -->
    <img src="@/assets/profile_black.svg" alt="Profile Icon" class="profile-icon" />
    <login-form @login="login" @goToSignUp="goToSignUp" @goToRecovery="goToRecovery" />
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
      if (username && password) {
        try {
          const response = await axios.post(
            'http://localhost:8000/api/login/',  // Login endpoint of the backend
            {
              username: username,
              password: password
            },
            {
              headers: {
                'Content-Type': 'application/json'
              }
            }
          );
          // Check if login was successful
          if (response.status === 200) {
            this.$emit('login');  // Trigger login event
            alert('Login successful');  // Optionally, you can redirect the user here
          } else {
            alert('Invalid credentials');
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
      this.$router.push('/signup');  // Redirect to sign up page
    },
    goToRecovery() {
      this.$router.push('/recovery-password');  // Redirect to password recovery page
    }
  }
};
</script>

<style scoped>
.login-page {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100vh;
    font-family: "Wix Madefor Display", sans-serif;
}

.profile-icon {
    width: 100px;
    height: 100px;
    margin-bottom: 20px;
    border-radius: 50%;
    border: 2px solid #ccc;
}
</style>

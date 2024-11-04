<template>
  <div class="login-page">
    <!-- Profile Icon -->
    <img src="@/assets/profile_picture.png" alt="Profile Icon" class="profile-icon" />
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
          const response = await axios.post('http://localhost:8000/api/auth/login/', {
            username,
            password
          });
          if (response.status === 200) {
            alert('Login successful');
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
      this.$router.push('/recovery-password');
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
}

.profile-icon {
  width: 100px;
  height: 100px;
  margin-bottom: 20px;
  border-radius: 50%;
  border: 2px solid #ccc;
}
</style>

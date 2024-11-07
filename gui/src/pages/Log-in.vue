<template>
  <div class="login-page">
    <!-- Profile Icon -->
    <img src="@/assets/profile_picture.png" alt="Profile Icon" class="profile-icon" />
    <login-form @login="login" @goToSignUp="goToSignUp" @goToRecovery="goToRecovery" />
    <span v-if="errorMessage" class="error-message">{{ errorMessage }}</span>
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
  data(){
    return{
      errorMessage: ''
    };
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
            //alert('Login successful');
            this.$router.push('/home');
          }
        } catch (error) {
          console.error('Login failed:', error);
          this.errorMessage = "Invalid username or password. Please try again.";
        }
      } else {
        this.errorMessage = "Please enter username and password";
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

.error-message {
  color: rgb(8, 34, 183);
  font-size: 14px;
  margin-top: 10px;
  text-align: center;
}

.profile-icon {
  width: 100px;
  height: 100px;
  margin-bottom: 20px;
  border-radius: 50%;
  border: 2px solid #ccc;
}
</style>

<template>
  <div class="login-page">
    <!-- Profile Icon -->
    <img src="@/assets/profile_black.svg" alt="Profile Icon" class="profile-icon" />
    <login-form @login="login" @goToSignUp="goToSignUp" @goToRecovery="goToRecovery" />
  </div>
</template>

<script>
import LoginForm from '../formats/login-form.vue';
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
          if (response.status === 200) { this.$emit('login'); //Don't move this for the moment:)
            alert('Login successful');
          } else { alert('Invalid credentials');
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
    padding-top: 220px;
    font-family: "Wix Madefor Display", sans-serif;
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

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
          axios.get(`http://localhost:8000/api/users/?username=${username}`).then(res => {
            // this.loginMessage = res.data;
            const user = res.data[0];
            console.log(user);
            if (user && user.password_hash === password) {
              alert('Login successful');
              this.$router.push('/home');
            } else {
              alert('Credenciales incorrectas.' + res.data);
            }
          })
          
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

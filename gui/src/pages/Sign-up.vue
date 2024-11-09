<template>
  <div class="signup-page">
    <!-- Profile Icon -->
    <img src="@/assets/profile_black.svg" alt="Profile Icon" class="profile-icon" />
    <sign-up-form @signUp="signUp" @goToLogin="goToLogin" />
  </div>
</template>

<script>
import SignUpForm from '../formats/signup-form.vue';
import axios from 'axios';

export default {
  name: 'SignUp',
  components: {
    SignUpForm
  },
  methods: {
    async signUp({ username, email, name, lastName, phone, curp, rfc, birthDate, password }) {
  if (username && email && password) {
    try {
      const response = await axios.post(
        'http://localhost:8000/api/register/',
        {
          user_name: username,
          email: email,
          name: name,
          last_name: lastName,
          phone: phone,
          curp: curp,
          rfc: rfc,
          birth_date: birthDate,
          password_hash: password
        },
        {
          headers: {
            'Content-Type': 'application/json'
          }
        }
      );

      if (response.status === 201) {
        alert('User registered successfully! Redirecting to login...');
        this.$router.push('/');
      } else {
        alert(response.data.error || 'Registration failed');
      }
    } catch (error) {
      console.error('Registration error:', error);
      alert(error.response?.data?.error || 'There was an issue with the registration. Please try again.');
    }
  } else {
    alert('Please fill in all required fields.');
  }
}

,
    goToLogin() {
      this.$router.push('/');
    }
  }
};
</script>

<style scoped>
.signup-page {
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

<template>
<div class="signup-page">
  <!-- Profile Icon -->
  <img src="@/assets/profile_picture.png" alt="Profile Icon" class="profile-icon" />
  <sign-up-form @signUp="signUp" @goToLogin="goToLogin" />
</div>
</template>

<script>
import SignUpForm from '../components/signup-form.vue';
import axios from 'axios';

export default {
  name: 'SignUp',
  components: {
    SignUpForm
  },
  methods: {
   async signUp({ username, email, password }) {
   // Temporary signup logic
   if (username && email && password) {	
     try {
       const response = await axios.post('https://here_goes_the_backend_url/signup', {
         username,
         email,
         password
       });
       // Handle the response from the backend (assuming it sends a success message or token)
       // 200 is a standard response code that indicates a successful HTTP request, specifically means 'OK'
       if (response.status === 200) {
         alert('User registered! Now, redirecting to login...');
         this.$router.push('/');
       }
     } catch (error) {
       // Handle any errors
       console.error('Signup failed:', error);
       alert('There was an issue with your signup. Please try again.');
     }
   } else {
     alert('Please fill all fields requiered.');
   }
   },
    goToLogin() {
      this.$router.push('/');
    }
  }
};
</script>

<style scoped>
/* Center the sign-up page */
.signup-page {
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

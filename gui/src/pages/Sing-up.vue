<template>
  <div class="signup-page">
    <!-- Profile Icon -->
    <img src="@/assets/profile_picture.png" alt="Profile Icon" class="profile-icon" />
    <sign-up-form @signUp="signUp" @goToLogin="goToLogin" />
  </div>
</template>

<script>
  import SignUpForm from '../components/signup-form.vue';
  
export default {
  name: 'SignUp',
  components: {
    SignUpForm
  },
  methods: {
    signUp({ username, email, password }) {
      // Temporary signup logic
      if (username && email && password) {
        alert('User registered! Now, redirecting to login...');
        this.$router.push('/');
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

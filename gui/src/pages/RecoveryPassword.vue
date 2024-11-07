<template>
  <div class="recovery-password-page">
    <!-- Profile Icon -->
    <img src="@/assets/profile_black.svg" alt="Profile Icon" class="profile-icon" />
    <recovery-form @sendCode="handleSendCode" @changePassword="goToLogin" @goToLogin="goToLogin"/>
  </div>
</template>

<script>
import RecoveryForm from '../components/recpassword-form.vue';

export default {
  name: 'RecoveryPassword',
  components: {
    RecoveryForm
  },
  methods: {
    handleSendCode({ email }) {
      console.log('Sending recovery code to:', email);
    },
    goToLogin() {
      this.$router.push('/');
    }
  }
};
</script>

<style scoped>
/* Center the recovery password page */
.recovery-password-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  font-family: "Wix Madefor Display", sans-serif;
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

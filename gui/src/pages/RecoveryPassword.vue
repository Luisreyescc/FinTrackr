<template>
<div class="recovery-password-page">
  <img src="@/assets/profile_white.svg" alt="Profile Icon" class="profile-icon" />

  <div class="message-container">
    <MessageAlerts
      v-for="(msg, index) in messages" 
      :key="msg.id" 
      :text="msg.text" 
      :type="msg.type" 
      @close="removeMessage(index)" />
  </div>
  
  <RecoveryForm
    :currentStep="currentStep"
    @sendCode="handleSendCode"
    @validateCode="handleValidateCode"
    @changePassword="goToLogin"
    @goToLogin="goToLogin" />
</div>
</template>

<script>
import RecoveryForm from '@/formats/recpassword-format.vue';
import MessageAlerts from '@/components/messages.vue';
import axios from 'axios';

export default {
  name: "RecoveryPassword",
  components: {
    RecoveryForm,
    MessageAlerts
  },
  data() {
    return {
      messages: [],
      currentStep: 1,
    };
  },
  methods: {
    addMessage(text, type = "neutral") {
      const id = Date.now();
      this.messages.push({ id, text, type });
    },
    removeMessage(index) {
      this.messages.splice(index, 1);
    },
    async handleSendCode({ username, email }) {
      try {
	const response = await axios.post(
          "http://url-for-send-code/",
          { username, email },
          { headers: { "Content-Type": "application/json" } }
        );
	if (response.status === 200) {
          this.addMessage("Recovery code sent successfully!", "success");
          this.currentStep = 2;
        }
      } catch (error) {
        this.addMessage("Failed to send recovery code. Please try again.", "error");
      }
    },
    async handleValidateCode({ recoveryCode }) {
      try {
	const response = await axios.post("htpp://url-for-validate-code/", { recoveryCode }, { headers: { "Content-Type": "application/json" } }
        );
	if (response.status === 200) {
          this.addMessage("Code validated successfully!", "success");
          this.currentStep = 3;
        }
      } catch (error) {
        this.addMessage("Invalid recovery code. Please try again.", "error");
      }
    },
    async handleChangePassword({ password }) {
      try {
        const response = await axios.post(
          "http://url-for-change-password/",
          { password },
          { headers: { "Content-Type": "application/json" } }
        );
        if (response.status === 200) {
          this.addMessage("Password changed successfully!", "success");
          this.goToLogin();
        }
      } catch (error) {
        this.addMessage("Failed to change password. Please try again.", "error");
      }
    },
    goToLogin() {
      this.$router.push("/");
    },
  }
};
</script>

<style scoped>
.recovery-password-page {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    background: #3B3B5A;
    font-family: "Wix Madefor Display", sans-serif;
}

.profile-icon {
    width: 120px;
    height: 120px;
    margin-bottom: -70px;
    border-radius: 50%;
    z-index: 1000;
    border: 2px solid rgba(255, 255, 255, 0.2);
    /*background: #3B3B5A;*/
    background: rgba(59, 59, 90, 0.1);
    backdrop-filter: blur(15px);
}
</style>

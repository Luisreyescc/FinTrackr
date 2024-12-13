<template>
<div class="recovery-password-page">
  <img src="@/assets/profile_white.svg" alt="Profile Icon" class="profile-icon"/>
  <div class="message-container">
    <MessageAlerts
      v-for="(msg, index) in messages" 
      :key="msg.id" 
      :text="msg.text" 
      :type="msg.type" 
      @close="removeMessage(index)"/>
  </div>
  <RecoveryForm
    :currentStep="currentStep"
    @sendCode="handleSendCode"
    @validateCode="handleValidateCode"
    @changePassword="handleChangePassword"
    @goToLogin="goToLogin"/>
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
      username: ""
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
      const requestData = { user_name: username, email: email };
      try {
          const response = await axios.post(
          "http://localhost:8000/api/send-code/",
          requestData,
          { headers: { "Content-Type": "application/json" } }
        );
        if (response.status === 200) {
          this.addMessage("Recovery code sent successfully to your email adress!", "success");
          this.currentStep = 2;
          this.username = username;
        }
      } catch (error) {
        this.addMessage("Failed to send recovery code. Please try again.", "error");
      }
    },
    async handleValidateCode({ recoveryCode }, callback) {
      const requestData = { user_name: this.username, recovery_code: recoveryCode };
      try {
        const response = await axios.post(
          "http://localhost:8000/api/validate-code/",
          requestData,
          { headers: { "Content-Type": "application/json" } }
        );
        if (response.status === 200) {
          this.addMessage("Code validated successfully!", "success");
          callback(true);
        }
      } catch (error) {
        this.addMessage("Invalid recovery code. Please try again.", "error");
        callback(false);
      }
    },
    async handleChangePassword({ password }) {
      const requestData = { user_name: this.username, password };
      try {
        const response = await axios.post(
          "http://localhost:8000/api/change-password/",
          requestData,
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
    }
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
    background: #25262B;
    font-family: "Wix Madefor Display", sans-serif;
}

.profile-icon {
    width: 120px;
    height: 120px;
    margin-bottom: -70px;
    border-radius: 50%;
    z-index: 1000;
    border: 2px solid rgba(255, 255, 255, 0.2);
    background: rgba(37, 38, 43, 0.1);
    backdrop-filter: blur(9px);
}
</style>

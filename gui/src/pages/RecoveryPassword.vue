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
  
  <RecoveryForm @sendCode="handleSendCode" @changePassword="goToLogin" @goToLogin="goToLogin" />
</div>
</template>

<script>
import RecoveryForm from '@/formats/recpassword-format.vue';
import MessageAlerts from '@/components/messages.vue';

export default {
  name: "RecoveryPassword",
  components: {
    RecoveryForm,
    MessageAlerts
  },
  data() {
    return {
      messages: []
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
    handleSendCode({ email }) {
      if (email) {
      this.addMessage(`Sending recovery code to: ${email}`, "neutral");
    } else {
      this.addMessage("Please provide a valid email address.", "error");
    }
  },
    goToLogin() {
      this.$router.push("/");
    },
  },
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

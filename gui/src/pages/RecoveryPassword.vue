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
//import axios from 'axios';

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
    /* async handleSendCode({ email }) {
      if (email) {
	try {
	  const valEmail = await axios.post(
            "http://localhost:8000/api/login/",
            { email: email },
            { headers: { "Content-Type": "application/json" } } );
	  this.addMessage('Sending recovery code to ${email}', "neutral");
	}
	catch (error) {
          this.addMessage('Sending code to ${email}', "error");
        }
      }
      async validateCode({ recoveryCode }) {
	if (recoveryCode) {
	  try {
	    const response = await axios.post("htpp://url-for-validate-code/");
	    if (response.status === 200) {
              const token = response.data.access;
              localStorage.setItem("token", token); this.addMessage("Login successful", "success"); this.$emit("login");
            } else {
              this.addMessage("Keycode not valid", "error");
            }
          } catch (error) {
            console.error("Login failed:", error);
            this.addMessage("Invalid username or password. Please try again.", "error");
	  }
	}
      }
    }, */
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

<template>
<div class="login-page">
  <img src="@/assets/profile_white.svg" alt="Profile Icon" class="profile-icon" />
  
  <div class="message-container">
    <MessageAlerts
      v-for="(msg, index) in messages" 
      :key="msg.id" 
      :text="msg.text" 
      :type="msg.type" 
      @close="removeMessage(index)" />
  </div>
  
  <LoginForm @login="login" @goToSignUp="goToSignUp" @goToRecovery="goToRecovery" />
</div>
</template>

<script>
import LoginForm from '@/formats/login-format.vue';
import MessageAlerts from '@/components/messages.vue';
import axios from 'axios';

export default {
  name: "LogIn",
  components: {
    LoginForm,
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
    async login({ username, password }) {
      if (username && password) {
        try {
          const response = await axios.post("http://localhost:8000/api/login/",
                                            { user_name: username, password: password },
                                            { headers: { "Content-Type": "application/json" }});
          console.log(response.data);
          if (response.status === 200) {
            const token = response.data.access;
            const isAdmin = response.data.is_admin;
            const userId = response.data.user_id;
            localStorage.setItem("token", token);
            localStorage.setItem("isAdmin", isAdmin);
            localStorage.setItem("user_id", userId);
            this.addMessage("Login successful", "success");
            this.$emit("login");
          } else {
            this.addMessage("Invalid username or password. Please try again.", "error");
          }
        } catch (error) {
          console.error("Login failed:", error);
          this.addMessage("Password or Email incorrect. Please try again.", "error");
        }
      } else {
        this.addMessage("Please enter username and password", "neutral");
      }
    },
    goToSignUp() {
      this.$router.push("/signup");
    },
    goToRecovery() {
      this.$router.push("/recovery-password");
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
    backdrop-filter: blur(15px);
}
</style>

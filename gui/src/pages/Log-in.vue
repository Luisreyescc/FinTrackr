<template>
  <div class="login-page">
    <!-- Profile Icon -->
    <img src="@/assets/profile_black.svg" alt="Profile Icon" class="profile-icon" />

    <div class="message-container">
      <MessageAlerts
        v-for="(msg, index) in messages" 
        :key="msg.id" 
        :text="msg.text" 
        :type="msg.type" 
        @close="removeMessage(index)" />
    </div>
    
    <login-form @login="login" @goToSignUp="goToSignUp" @goToRecovery="goToRecovery" />
  </div>
</template>

<script>
import LoginForm from '@/formats/login-form.vue';
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
          const response = await axios.post(
            "http://localhost:8000/api/login/", // Login endpoint of the backend
            {
              user_name: username,
              password: password,
            },
            {
              headers: {
                "Content-Type": "application/json",
              },
            },
          );
          console.log(response.data);
          if (response.status === 200) {
            const token = response.data.access;
            localStorage.setItem("token", token); this.addMessage("Login successful", "success"); this.$emit("login");
          } else {
            this.addMessage("Invalid credentials", "error");
          }
        } catch (error) {
          console.error("Login failed:", error);
          this.addMessage("Invalid username or password. Please try again.", "error");
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
    padding-top: 220px;
    font-family: "Wix Madefor Display", sans-serif;
}

.error-message {
    color: rgb(8, 34, 183);
    font-size: 14px;
    margin-top: 10px;
    text-align: center;
}

.profile-icon {
  width: 100px;
  height: 100px;
  margin-bottom: 20px;
  border-radius: 50%;
  border: 2px solid #ccc;
}
</style>

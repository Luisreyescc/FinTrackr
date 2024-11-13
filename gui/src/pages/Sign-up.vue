<template>
<div class="signup-page">
  <img src="@/assets/profile_black.svg" alt="Profile Icon" class="profile-icon" />
  
  <div class="message-container">
    <MessageAlerts
      v-for="(msg, index) in messages" 
      :key="msg.id" 
      :text="msg.text" 
      :type="msg.type" 
      @close="removeMessage(index)"
      />
  </div>
  
  <sign-up-form @signUp="signUp" @goToLogin="goToLogin" />
</div>
</template>

<script>
import SignUpForm from '@/formats/signup-form.vue';
import MessageAlerts from '@/components/messages.vue';
import apiClient from "@/apiClient.js";

export default {
  name: "SignUp",
  components: {
    SignUpForm,
    MessageAlerts
  },
  data() {
    return {
      messages: [] // Array to store messages
    };
  },
  methods: {
    addMessage(text, type = "neutral") {
      const id = Date.now(); // ID único basado en el tiempo
      this.messages.push({ id, text, type });
    },
    removeMessage(index) {
      this.messages.splice(index, 1);
    },
    async signUp({ username, email, password, password2 }) {
      if (username && email && password && password2) {
        try {
          const response = await apiClient.post("register/", {
            user_name: username,
            email: email,
            password: password,
            password2: password2,
          });

          if (response.status === 201) {
            this.addMessage("User registered successfully! Redirecting to login...", "success");
            this.$router.push("/login");
          } else {
            this.addMessage(response.data.error || "Registration failed", "error");
          }
        } catch (error) {
          console.error("Registration error:", error);
          if (error.response && error.response.data) {
            const errors = [];
            for (const key in error.response.data) {
              errors.push(`${key}: ${error.response.data[key]}`);
            }
            this.addMessage(errors.join("\n"), "error");
          } else { this.addMessage("There was an issue with your registration. Please try again.", "error"); }
        }
      } else {
        this.addMessage("Please fill in all required fields.", "neutral");
      }
    },
    goToLogin() {
      this.$router.push("/login");
    },
  },
};
</script>

<style scoped>
.signup-page {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding-top: 190px;
    font-family: "Wix Madefor Display", sans-serif;
}

.profile-icon {
    width: 100px;
    height: 100px;
    margin-bottom: 20px;
    border-radius: 50%;
    border: 2px solid #ccc;
}

.message-container {
    width: 100%;
    max-width: 400px;
    position: absolute;
    top: 20px;
}
</style>

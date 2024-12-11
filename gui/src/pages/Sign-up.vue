<template>
<div class="signup-page">
  <div class="brand-section">
    <img src="@/assets/title.svg" alt="Profile Icon" class="title"/>
    <P class="slogan">Keep track of your finances safely, quickly and easily</P>
  </div>
  <div class="signup-content">
    <img src="@/assets/profile_white.svg" alt="Profile Icon" class="profile-icon"/>
    <div class="message-container">
      <MessageAlerts
	v-for="(msg, index) in messages" 
	:key="msg.id" 
	:text="msg.text" 
	:type="msg.type" 
	@close="removeMessage(index)"/>
    </div>
    <SignUpForm @signUp="signUp" @goToLogin="goToLogin"/>
  </div>
</div>
</template>

<script>
import axios from "axios";
import SignUpForm from '@/formats/signup-format.vue';
import MessageAlerts from '@/components/messages.vue';
import apiClient from "@/apiClient.js";

export default {
  name: "SignUp",
  components: {
    SignUpForm,
    MessageAlerts
  },
  data() {
    return { messages: [] };
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
          this.addMessage("Recovery code sent successfully!", "success");
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
    async signUp({ username, email, password, password2, admin_user }) {
      if (username && email && password && password2) {
        try {
          const response = await apiClient.post("register/",
						{ user_name: username,
                                                  email: email,
                                                  password: password,
                                                  password2: password2,
                                                  admin_user: admin_user });
	  if (response.status === 201) {
            const responseLog = await axios.post("http://localhost:8000/api/login/",
                                                 { user_name: username, password: password },
                                                 { headers: { "Content-Type": "application/json" }});
            console.log(responseLog.data);
            if (responseLog.status === 200) {
              const token = responseLog.data.access;
              await axios.get("http://localhost:8000/api/pdf/?action=start&interval=1&unit=months&first=1",
                              { headers: { Authorization: `Bearer ${token}` } });
              this.addMessage("Login successful", "success");
            } else {
              this.addMessage("Invalid username or password. Please try again.", "error");
            }
            this.addMessage("User registered successfully! Redirecting to login...", "success");
            setTimeout(() => { this.$router.push("/login") }, 2500);
          } else {
            this.addMessage(response.data.error || "Registration failed", "error");
          }
        } catch (error) {
          console.error("Registration error:", error);
          if (error.response && error.response.data) {
            const errors = [];
            for (const key in error.response.data)
              errors.push(`${key}: ${error.response.data[key]}`);
            this.addMessage(errors.join("\n"), "error");
          } else {
            this.addMessage("There was an issue with your registration. Please try again.", "error");
          }
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
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    background: #25262B;
    font-family: "Wix Madefor Display", sans-serif;
    gap: 20px;
}

.brand-section {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    color: white;
}

.title {
    display: flex-start;
    width: 320px;
    height: 70px;
    z-index: 1000;
    margin-bottom: 10px;
    border: none;
    background: #25262B;
}

.slogan {
    font-size: 20px;
    color: white;
    font-family: "Wix Madefor Display", sans-serif;
}

.signup-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 60px;
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

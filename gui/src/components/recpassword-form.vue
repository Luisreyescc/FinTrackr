<template>
  <div class="recovery-form">
    <label for="username">Username</label>
    <input
      v-model="username"
      type="text"
      id="username"
      placeholder="Insert username..."
    />
    <label for="email">E-mail</label>
    <input
      v-model="email"
      type="email"
      id="email"
      placeholder="Insert email..."
    />

    <!-- Send Code Button -->
    <button class="send-code-btn" @click="sendCode">Send code</button>
    <!-- Recovery Code Input, shown after Send Code is clicked -->
    <label v-if="codeSent" for="recovery-code">Recovery Code</label>
    <input
      v-if="codeSent"
      v-model="recoveryCode"
      type="text"
      id="recovery-code"
      placeholder="Enter recovery code..."
    />
    <!-- Change Password Button -->
    <button v-if="codeSent" class="change-password-btn" @click="changePassword">
      Change Password
    </button>
    <button class="login-btn" @click="$emit('goToLogin')">Log-in</button>
  </div>
</template>

<script>
export default {
  name: "RecoveryForm",
  data() {
    return {
      username: "",
      email: "",
      recoveryCode: "",
      codeSent: false, // State to track if the code has been sent
    };
  },
  methods: {
    sendCode() {
      if (this.username && this.email) {
        this.codeSent = true;
        alert("A recovery code has been sent to your email!");
        // Emit an event to the parent if needed
        this.$emit("sendCode", { username: this.username, email: this.email });
      } else {
        alert("Please enter both username and email.");
      }
    },
    changePassword() {
      if (this.recoveryCode) {
        alert("Password changed successfully! Redirecting to login...");
        this.$emit("changePassword");
      } else {
        alert("Please enter the recovery code.");
      }
    },
  },
};
</script>

<style scoped>
/* Recovery form styling */
.recovery-form {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  width: 300px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  font-family: "Wix Madefor Display", sans-serif;
}

label {
  align-self: flex-start;
  margin-bottom: 5px;
  font-weight: bold;
  color: #333;
  font-family: "Wix Madefor Display", sans-serif;
}

input {
  width: 100%;
  padding: 10px;
  margin-bottom: 15px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  color: #333;
  font-family: "Wix Madefor Display", sans-serif;
}

button {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  width: 100%;
}

.send-code-btn {
  background-color: #4caf50;
  color: white;
  margin-bottom: 15px;
  font-family: "Wix Madefor Display", sans-serif;
}

.change-password-btn {
  background-color: #333;
  color: white;
  font-family: "Wix Madefor Display", sans-serif;
}

login-btn {
  background-color: #0033cc;
  color: white;
  font-family: "Wix Madefor Display", sans-serif;
}

button:hover {
  opacity: 0.9;
}
</style>

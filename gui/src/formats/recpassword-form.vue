<template>
  <div class="recovery-form">
    <label for="username">Username</label>
    <div class="username-container">
      <span class="user-icon gg-user"></span>
      <input
	v-model="username"
	type="text"
	id="username"
	placeholder="Insert username..."
	:class="{ 'input-error': usernameError, 'padded-input': true }"
	@input="clearError('username')" />
    </div>
    <span v-if="usernameError" class="error-message">{{ usernameError }}</span>
    <label for="email">E-mail</label>
    <div class="email-container">
      <span class="email-icon gg-mail"></span>
      <input
	v-model="email"
	type="email"
	id="email"
	placeholder="Insert email..."
	:class="{ 'input-error': emailError, 'padded-input': true }"
	@input="clearError('email')" />
    </div>
    <span v-if="emailError" class="error-message">{{ emailError }}</span>
    
    <button class="send-code-btn" @click="sendCode">Send code</button>
    <!-- Recovery Code Input, shown after Send Code is clicked -->
    <label v-if="codeSent" for="recovery-code">Recovery Code</label>
    <div v-if="codeSent" class="recovery-container">
    <span class="key-icon gg-key"></span>
    <input
      v-model="recoveryCode"
      type="text"
      id="recovery-code"
      placeholder="Enter recovery code..."
      :class="{ 'input-error': keyError, 'padded-input': true }"
      @input="clearError('recoveryCode')" />
    </div>
    <span v-if="keyError" class="error-message">{{ keyError }}</span>
    
    <button v-if="codeSent" class="change-password-btn" @click="changePassword">Change Password</button>
    <button class="login-btn" @click="$emit('goToLogin')">Log-in</button>
  </div>
</template>

<script>
import '@/css/key.css';
export default {
  name: 'RecoveryForm',
  data() {
    return {
      username: '',
      email: '',
      recoveryCode: '',
      codeSent: false, // State to track if the code has been sent
      usernameError: '',
      emailError: '',
      keyError: ''
    };
  },
  methods: {
    sendCode() {
      this.usernameError = '';
      this.emailError = '';     
      if (!this.username)
	this.usernameError = 'Username is required';
      if (!this.email)
	this.emailError = 'Email is required';
      if (this.username && this.email) {
        this.codeSent = true;
        alert('A recovery code has been sent to your email!');
        // Emit an event to the parent if needed
        this.$emit('sendCode', { username: this.username, email: this.email });
      }
    },
    changePassword() {
      this.keyError = '';
      if (this.recoveryCode) {
        alert('Password changed successfully! Redirecting to login...');
        this.$emit('changePassword');
      } else {
	this.keyError = 'Please insert the code sent to your e-mail';
      }
    },
    clearError(field) {
      // Clear specific error messages when the user starts typing
      if (field === 'username')
	this.usernameError = '';
      if (field === 'email')
	this.emailError = '';
      if (field === 'recoveryCode')
	this.keyError = '';
    },
  }
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

.input-error {
    border-color: #E42121;
}

.error-message {
    color: #E42121;
    font-size: 12px;
    align-self: flex-start;
    margin-top: -10px;
    margin-bottom: 10px;
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
  background-color: #4CAF50;
  color: white;
  margin-bottom: 15px;
  font-family: "Wix Madefor Display", sans-serif;
}

.change-password-btn {
  background-color: #BF9F00;
  color: white;
  font-family: "Wix Madefor Display", sans-serif;
}

.login-btn {
  background-color: #333;
  color: white;
  margin-top: 15px;
  font-family: "Wix Madefor Display", sans-serif;
}

button:hover {
  opacity: 0.9;
}

.username-container, .email-container, .recovery-container {
  display: flex;
  align-items: center;
  position: relative;
  width: 108%;
}

.user-icon {
    position: absolute;
    left: 15px;
    color: #555;
    font-size: 18px;
    margin-top: -5%;
    pointer-events: none;
}

.email-icon {
    position: absolute;
    left: 13px;
    color: #555;
    font-size: 18px;
    margin-top: -4%;
    pointer-events: none;
}

.key-icon {
  position: absolute;
  left: 25px;
  color: #555;
  font-size: 18px;
  margin-top: -4%;
  pointer-events: none;
}

.padded-input {
  padding-left: 40px;
}
</style>

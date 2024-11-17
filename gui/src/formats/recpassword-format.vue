<template>
<div class="recovery-form">
  <h2 class="form-title">Recovery Password</h2>
  <!-- We define the Recovery pages in state-->
  <div v-if="currentStep === 1">
    <div class="username-container">    
      <font-awesome-icon class="user-icon" :icon="['fas', 'user']" />
      <input
	v-model="username"
	type="text"
	id="username"
	placeholder="Username"
	:class="{ 'input-error': usernameError, 'padded-input': true }"
	@input="clearError('username')" />
    </div>
    <div class="email-container">
      <font-awesome-icon class="email-icon" :icon="['fas', 'envelope']" />
      <input
	v-model="email"
	type="email"
	id="email"
	placeholder="Email"
	:class="{ 'input-error': emailError, 'padded-input': true }"
	@input="validateEmail" />
    </div>
    <button class="send-code-btn" @click="sendCode">Send code</button>
  </div>
    
  
  <div v-if="currentStep === 2" class="recovery-container">
    <font-awesome-icon class="key-icon" :icon="['fas', 'key']" />
    <input
      v-model="recoveryCode"
      type="text"
      id="recovery-code"
      placeholder="Recovery code"
      :class="{ 'input-error': keyError, 'padded-input': true }"
      @input="clearError('recoveryCode')" />
    <button class="validate-code-btn" @click="validateCode">Validate Code</button>
  </div>
  
  <div v-if="currentStep === 3">
    <div class="password-container">
      <input
	v-model="password"
	:type="showPassword ? 'text' : 'password'"
	id="password"
	placeholder="New password"
	:class="{ 'input-error': passwordError, 'padded-input': true }"
	@input="clearError('password')" />
      <button
	type="button" 
	class="show-password-btn" 
	@click="togglePasswordVisibility"
	aria-label="Show or Hide Password" >
	<span :class="{ 'gg-eye': true, 'gg-eye-alt': showPassword }"></span>
      </button>
    </div>
    <div class="password-container">
      <input
	v-model="password2"
	:type="showConfirmPassword ? 'text': 'password'"
	id="password2"
	placeholder="Confirm newn password"
	:class="{ 'input-error': confirmPasswordError, 'padded-input': true }"
	@input="clearError('password2')" />
      <button 
	type="button" 
	class="show-password-btn" 
	@click="toggleConfirmPasswordVisibility"
	aria-label="Show or Hide Confirm Password">
      <span :class="{ 'gg-eye': true, 'gg-eye-alt': showConfirmPassword }"></span>
      </button>
      <button v-if="codeSent" class="change-password-btn" @click="changePassword">Change Password</button>
    </div>
  </div>

  <button class="login-btn" @click="$emit('goToLogin')">Log-in</button>
</div>

<div class="message-container">
  <MessageAlerts
    v-for="(msg, index) in messages" 
    :key="msg.id" 
    :text="msg.text" 
    :type="msg.type" 
    @close="removeMessage(index)" />
</div>
</template>

<script>
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import MessageAlerts from '@/components/messages.vue';
import isEmail from "validator/lib/isEmail";

export default {
  name: 'RecoveryForm',
  components: {
    FontAwesomeIcon,
    MessageAlerts
  },
  data() {
    return {
      currentStep: 1,
      username: '',
      email: '',
      recoveryCode: '',
      password: '',
      password2: '',
      codeSent: false, // State to track if the code has been sent
      usernameError: false,
      emailError: false,
      keyError: false,
      passwordError: false,
      confirmPasswordError: false,
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
    clearError(field) {
      this[`${field}Error`] = false; // This instead of doing many if's
    },
    sendCode() {
      if (this.validateInputs() && this.validateEmail()) {
	this.currentStep = 2; // Next state of the page, validate key code
        this.$emit('sendCode', { username: this.username, email: this.email });
      }
    },
    validateCode() {
      if (!this.recoveryCode) {
        this.keyError = true;
        this.addMessage("Recovery code is required.", "error");
      } else {
        this.currentStep = 3; // Next state of the page, create ne password
        this.addMessage("Code validated successfully.", "success");
      }
    },
    changePassword() {
      let isValid = true;
      if (!this.password) {
        this.addMessage("Password is required.", "error");
        this.passwordError = true;
        isValid = false;
      }
      if (!this.password2) {
        this.addMessage("Confirm password is required.", "error");
        this.confirmPasswordError = true;
        isValid = false;
      }
      if (this.password !== this.password2) {
        this.addMessage("Passwords do not match.", "error");
        this.passwordError = true;
        this.confirmPasswordError = true;
        isValid = false;
      }
      if (isValid) {
        this.addMessage("Password changed successfully.", "success");
        this.$emit('changePassword');
      }
    },
    validateInputs() {
      let isValid = true;

      if (!this.username) {
        this.addMessage("Username is required.", "error");
        this.usernameError = true;
        isValid = false;
      } else if (this.username.length < 3 || this.username.length > 16) {
        this.addMessage("Username must be 3-16 characters long.", "error");
        this.usernameError = true;
        isValid = false;
      }
      if (!this.email) {
        this.addMessage("Email is required.", "error");
        this.emailError = true;
        isValid = false;
      }
      
      return isValid;
    },
    validateEmail() {
      if (this.email) {
	if (isEmail(this.email)) {
          this.emailError = false;
          return true;
	} else {
          this.addMessage("Invalid email format.", "error");
          this.emailError = true;
          return false;
	}
      }
      
      return true;
    },
    togglePasswordVisibility() {
      this.showPassword = !this.showPassword;
    },
    toggleConfirmPasswordVisibility() {
      this.showConfirmPassword = !this.showConfirmPassword;
    }
}
};
</script>

<style scoped>
.recovery-form {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20px;
    border: 2px solid rgba(255, 255, 255, 0.2);
    border-radius: 12px;
    width: 350px;
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(15px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    font-family: "Wix Madefor Display", sans-serif;
}

.form-title {
    margin-top: 70px;
    color: white;
    font-size: 32px;
    font-family: "Wix Madefor Display", sans-serif;
}

input {
    width: 50%;
    padding: 14px;
    margin-bottom: 20px;
    background-color: transparent;
    border: none;
    outline: none;
    border-bottom: 2px solid white;
    font-family: "Wix Madefor Display", sans-serif;
}

.input-error {
    border-color: #D55C5C;
}

.username-container,
.email-container,
.password-container {
    position: relative;
    width: 130%;
    color: white;
    left: -50px;
    font-size: 18px;
    font-family: "Wix Madefor Display", sans-serif;
}

.recovery-container {
    position: relative;
    width: 110%;
    left: -5px;
    color: white;
    font-size: 18px;
    font-family: "Wix Madefor Display", sans-serif;
}

.username-container input,
.email-container input,
.recovery-container input,
.password-container input{
    color: white;
    font-size: 18px;
    font-family: "Wix Madefor Display", sans-serif;
}

.username-container input::placeholder {
    color: white;
    font-size: 18px;
}

.email-container input::placeholder {
    color: white;
    font-size: 18px;
}

.recovery-container input::placeholder {
    color: white;
    font-size: 18px;
}

.password-container input::placeholder {
    color: white;
    font-size: 18px;
}

.user-icon, .email-icon, .key-icon {
    position: relative;
    right: -25px;
    top: 35%;
    color: white;
    font-size: 18px;
    pointer-events: none;
}

.show-password-btn {
    position: absolute;
    left: 50px;
    top: -10%;
    background: none;
    border: none;
    color:white;
    cursor: pointer;
    font-size: 20px;
}

.padded-input {
    padding-left: 40px;
}

button {
    width: 65%;
    padding: 10px 20px;
    border: none;
    border-radius: 4px;
    font-size: 14px;
    margin-top: 15px;
    cursor: pointer;
}

.send-code-btn {
    padding: 10px 20px;
    width: 75%;
    border-radius: 20px;
    background-color: white;
    border: 2px solid white;
    margin-bottom: 15px;
    cursor: pointer;
    color: #333;
    font-size: 18px;
    font-family: "Wix Madefor Display", sans-serif;
}


.change-password-btn {
    padding: 10px 20px;
    border-radius: 20px;
    background-color: #BF9F00;
    border: 2px solid #BF9F00;
    margin-bottom: 15px;
    cursor: pointer;
    color: white;
    font-size: 18px;
    font-family: "Wix Madefor Display", sans-serif;
}

.login-btn {
    padding: 10px 20px;
    border-radius: 20px;
    background-color: #333;
    border: 2px solid #333;
    margin-top: 20px;
    margin-bottom: 20px;
    cursor: pointer;
    color: white;
    font-size: 18px;
    font-family: "Wix Madefor Display", sans-serif;
}

.validate-code-btn {
    padding: 10px 20px;
    border-radius: 20px;
    background-color: #BF9F00;
    border: 2px solid #BF9F00;
    margin-bottom: 15px;
    cursor: pointer;
    color: white;
    font-size: 18px;
    font-family: "Wix Madefor Display", sans-serif;
}

button:hover {
  opacity: 0.9;
}
</style>

<template>
<div class="recovery-form">
  <h2 class="form-title">Recovery Password</h2>
  <div v-if="currentStep === 1">
    <div class="username-container">    
      <font-awesome-icon class="user-icon" :icon="['fas', 'user']"/>
      <input
	v-model="username"
	type="text"
	id="username"
	placeholder="Username"
	:class="{ 'input-error': usernameError, 'padded-input': true }"
	@input="clearError('username')"/>
    </div>
    <span v-if="usernameError" class="error-message">{{ usernameError }}</span>
    
    <div class="email-container">
      <font-awesome-icon class="email-icon" :icon="['fas', 'envelope']"/>
      <input
	v-model="email"
	type="email"
	id="email"
	placeholder="Email"
	:class="{ 'input-error': emailError, 'padded-input': true }"
	@input="clearError('email')"/>
    </div>
    <span v-if="emailError" class="error-message">{{ emailError }}</span>
    <button class="send-code-btn" @click="sendCode">Send code</button>
  </div>
  
  <div v-if="currentStep === 2" class="recovery-container">
    <font-awesome-icon class="key-icon" :icon="['fas', 'key']"/>
    <input
      v-model="recoveryCode"
      type="text"
      id="recovery-code"
      placeholder="Recovery code"
      :class="{ 'input-error': keyError, 'padded-input': true }"
      @input="clearError('recoveryCode')"/>
    <span v-if="keyError" class="error-message">{{ keyError }}</span>
    <div class="code-buttons">
      <button class="resend-code-btn" @click="resendCode">Resend Code</button>
      <button class="validate-code-btn" @click="validateCode">Validate Code</button>
    </div>
  </div>
  
  <div v-if="currentStep === 3">
    <div class="password-container">
      <input
	v-model="password"
	:type="showPassword ? 'text' : 'password'"
	id="password"
	placeholder="New password"
	:class="{ 'input-error': passwordError, 'padded-input': true }"
	@input="clearError('password')"/>
      <button
	type="button" 
	class="show-password-btn" 
	@click="togglePasswordVisibility"
	aria-label="Show or Hide Password">
	<span :class="{ 'gg-eye': true, 'gg-eye-alt': showPassword }"></span>
      </button>
    </div>
    <span v-if="passwordError" class="error-message">{{ passwordError }}</span>
    
    <div class="password-container">
      <input
	v-model="password2"
	:type="showConfirmPassword ? 'text': 'password'"
	id="password2"
	placeholder="Confirm new password"
	:class="{ 'input-error': confirmPasswordError, 'padded-input': true }"
	@input="clearError('password2')"/>
      <button 
	type="button" 
	class="show-password-btn" 
	@click="toggleConfirmPasswordVisibility"
	aria-label="Show or Hide Confirm Password">
      <span :class="{ 'gg-eye': true, 'gg-eye-alt': showConfirmPassword }"></span>
      </button>
    </div>
    <span v-if="confirmPasswordError" class="error-message">{{ confirmPasswordError }}</span>
    <button class="change-password-btn" @click="changePassword">Change Password</button>
  </div>

  <div class="return-login">
    <div class="divider">
      <span>or return to</span>
    </div>
    <button class="login-btn" @click="$emit('goToLogin')">Log-in</button>
  </div>
</div>
</template>

<script>
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import axios from 'axios';

export default {
  name: 'RecoveryForm',
  components: { FontAwesomeIcon },
  data() {
    return {
      currentStep: 1,
      username: "",
      email: "",
      recoveryCode: "",
      password: "",
      password2: "",
      codeSent: false, // State to track if the code has been sent
      usernameError: "",
      emailError: "",
      keyError: "",
      passwordError: "",
      confirmPasswordError: "",
      showPassword: false,
      showConfirmPassword: false,
    };
  },
  methods: {
    clearError(field) {
      if (field === "username")
	this.usernameError = "";
      if (field === "email")
	this.emailError = "";
      if (field === 'recoveryCode')
	this.keyError = "";
      if (field === 'password')
	this.passwordError = "";
      if (field === 'password2')
	this.confirmPasswordError = "";
    },
    async sendCode() {
      this.usernameError = "";
      this.emailError = "";
      if (!this.username)
	this.usernameError = "Username is required.";
      if (!this.email)
	this.emailError = "Email is required.";
      if (!this.usernameError && !this.emailError) {
        try {
          const response = await axios.post("http://localhost:8000/api/check-user-email-association/", {
            user_name: this.username,
            email: this.email
          });
          
          if (response.status === 200) {
	this.$emit('sendCode', { username: this.username, email: this.email });
	this.currentStep = 2; // Next state of the page, validate key code
      }
        } catch (error) {
          if (error.response && error.response.data && error.response.data.error) {
            if (error.response.data.error.includes("Username")) {
              this.usernameError = error.response.data.error;
            } else if (error.response.data.error.includes("Email")) {
              this.emailError = error.response.data.error;
            }
          } else {
            this.$emit('addMessage', "There was an issue checking user-email association. Please try again.", "error");
          }
        }
      }
    },
    validateCode() {
      this.keyError = "";
      if (!this.recoveryCode) {
	this.keyError = "The recovery code is required";
      } else {
	this.$emit("validateCode", { recoveryCode: this.recoveryCode }, (isValid) => {
          if (isValid)
            this.currentStep = 3;
          else
            this.keyError = "";
        });
      }
    },
    changePassword() {
      this.passwordError = "";
      this.confirmPasswordError = "";
      
      if (!this.password)
	this.passwordError = 'Password is required';
      if (!this.password2)
	this.confirmPasswordError = 'Confirm password is required';
      if (this.password && this.password2 && this.password !== this.password2) {
	this.passwordError = 'Passwords don\'t match';
	this.confirmPasswordError = 'Passwords don\'t match';
      }
      if (!this.passwordError && !this.confirmPasswordError)
        this.$emit("changePassword", { password: this.password });
    },
    togglePasswordVisibility() {
      this.showPassword = !this.showPassword;
    },
    toggleConfirmPasswordVisibility() {
      this.showConfirmPassword = !this.showConfirmPassword;
    },
    resendCode() {
      this.$emit('sendCode', { username: this.username, email: this.email });
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

.error-message {
    color: #D55C5C;
    font-size: 14px;
    align-self: center;
    margin-top: -10px;
    margin-bottom: 10px;
}

.username-container,
.email-container {
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
.recovery-container input {
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
    padding: 15px 30px;
    width: 75%;
    border-radius: 3px;
    background-color: white;
    border: 2px solid white;
    margin-bottom: 15px;
    cursor: pointer;
    color: #25262B;
    font-size: 18px;
    font-family: "Wix Madefor Display", sans-serif;
}

.change-password-btn {
    padding: 15px 20px;
    border-radius: 3px;
    background-color: #BF9F00;
    border: 2px solid #BF9F00;
    margin-bottom: 15px;
    cursor: pointer;
    color: white;
    font-size: 18px;
    font-family: "Wix Madefor Display", sans-serif;
}

.divider {
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 10px 0;
    width: 100%;
    position: relative;
}

.return-login {
    width: 60%;
    display: flex;
    margin-top: 5px;
    flex-direction: column;
}

.divider::before,
.divider::after {
    content: '';
    flex: 1;
    height: 1px;
    background-color: white;
    margin: 0 10px;
}

.divider span {
    font-size: 14px;
    color: white;
    font-family: "Wix Madefor Display", sans-serif;
    font-weight: bold;
}

.login-btn {
    width: 100%;
    padding: 15px 30px;
    border-radius: 3px;
    background-color: #25262B;
    border: 2px solid #25262B;
    margin-top: 5px;
    margin-bottom: 20px;
    cursor: pointer;
    color: white;
    font-size: 18px;
    font-family: "Wix Madefor Display", sans-serif;
}

.code-buttons{
    margin-left: 22px;
    width: 90%;
    display: flex;
    gap: 10px;
    justify-content: space-between;
}

.resend-code-btn,
.validate-code-btn {
    padding: 13px 15px;
    border-radius: 3px;
    cursor: pointer;
    color: white;
    font-size: 18px;
    font-family: "Wix Madefor Display", sans-serif;
}

.resend-code-btn {
    background-color: #D131C6;
    border: 2px solid #D131C6;
}

.validate-code-btn {
    background-color: #BF9F00;
    border: 2px solid #BF9F00;
}

button:hover {
  opacity: 0.9;
}

.password-container {
    display: flex;
    align-items: center;
    position: relative;
    justify-content: space-between;
    width: 100%;
    color: white;
    font-size: 18px;
    margin-bottom: 20px;
    font-family: "Wix Madefor Display", sans-serif;
}

.password-container input {
    flex: 1;
    padding-left: 40px;
    padding-right: 40px;
    color: white;
    font-size: 18px;
    font-family: "Wix Madefor Display", sans-serif;
}

.show-password-btn {
    position: absolute;
    left: 5px;
    top: 2%;
    background: none;
    border: none;
    color: white;
    cursor: pointer;
    font-size: 20px;
    padding: 0;
    width: auto; 
    height: auto;
}
</style>

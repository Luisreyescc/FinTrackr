<template>    
<div class="signup-form">
  <h2 class="form-title">Sign Up</h2>
  <span class="admin-status">New account as: {{ isAdminUser ? 'Admin' : 'User' }}</span>
  
  <div class="username-container">
    <font-awesome-icon class="user-icon" :icon="['fas', 'user']"/>
    <input
      v-model="username"
      type="text"
      id="username"
      placeholder="Your username"
      :class="{ 'input-error': usernameError, 'padded-input': true }"
      @input="validateUser"/>
  </div>
  <span v-if="usernameError" class="error-message">{{ usernameError }}</span>
  
  <div class="email-container">
    <font-awesome-icon class="email-icon" :icon="['fas', 'envelope']"/>
    <input
      v-model="email"
      type="email"
      id="email"
      placeholder="Your email"
      :class="{ 'input-error': emailError, 'padded-input': true }"
      @input="validateEmail"/>
  </div>
  <span v-if="emailError" class="error-message">{{ emailError }}</span>
  
  <div class="password-container">
    <input
      v-model="password"
      :type="showPassword ? 'text' : 'password'"
      id="password"
      placeholder="Your password"
      :class="{ 'input-error': passwordError, 'padded-input': true }"
      @input="clearError('password')"/>
    <button
      type="button" 
      class="show-password-btn" 
      @click="togglePasswordVisibility"
      aria-label="Show or Hide Password" >
      <span :class="{ 'gg-eye': true, 'gg-eye-alt': showPassword }"></span>
    </button>
  </div>
  <span v-if="passwordError" class="error-message">{{ passwordError }}</span>
  
  <div class="password-container">
    <input
      v-model="password2"
      :type="showConfirmPassword ? 'text': 'password'"
      id="password2"
      placeholder="Confirm your password"
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

  <div class="admin-toggle-container">
    <button class="admin-toggle-btn" @click="toggleAdminUser">
      {{ isAdminUser ? ' Change to Casual User' : 'Change to Admin User' }}
    </button>
    
  </div>
  
  <div class="button-group">
    <button class="accept-btn" @click="emitSignUp">Accept</button>
    <div class="divider">
      <span>or return to</span>
    </div>
    <button class="login-btn" @click="$emit('goToLogin')">Log-In</button>
  </div>
</div>
</template>

<script>
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import isEmail from "validator/lib/isEmail";

export default {
  name: "SignUpForm",
  components: { FontAwesomeIcon },
  data() {
    return {
      username: "",
      email: "",
      password: "",
      password2: "",
      usernameError: "",
      emailError: "",
      passwordError: "",
      confirmPasswordError: "",
      showPassword: false,
      showConfirmPassword: false,
      isAdminUser: false
    };
  },
  methods: {
    clearError(field) {
      if (field === 'username')
	this.usernameError = '';
      if (field === 'email')
	this.emailError = '';
      if (field === 'password')
	this.passwordError = '';
      if (field === 'password2')
	this.confirmPasswordError = '';
    },
    emitSignUp() {
      this.usernameError = '';
      this.emailError = '';
      this.passwordError = '';
      this.confirmPasswordError = '';
      if (!this.username)
	this.usernameError = 'Username is required';
      else if (this.username.length < 3)
	this.usernameError = 'Username requieres at least 3 characters';
      if (!this.email)
	this.emailError = 'Email is required';
      else if (!isEmail(this.email))
	this.emailError = 'Invalid email format';
      if (!this.password)
	this.passwordError = 'Password is required';
      if (!this.password2)
	this.confirmPasswordError = 'Confirm password is required';
      if (this.password && this.password2 && this.password !== this.password2) {
	this.passwordError = 'Passwords don\'t match';
	this.confirmPasswordError = 'Passwords don\'t match';
      }
      
      if (!this.usernameError && !this.emailError && !this.passwordError && !this.confirmPasswordError) {
        this.$emit("signUp",
                   { username: this.username,
                     email: this.email,
                     password: this.password,
                     password2: this.password2,
                     admin_user: this.isAdminUser});
      }
    },
    validateUsername() {
      this.usernameError = '';
      if (this.username.length > 0 && this.username.length < 3 || this.username.length > 16) {
        this.usernameError = 'Username must be 3-16 characters long';
      }
    },
    validateEmail() {
      this.emailError = '';
      if (this.email && !isEmail(this.email)) {
        this.emailError = 'Invalid email format';
      }
    },
    togglePasswordVisibility() {
      this.showPassword = !this.showPassword;
    },
    toggleConfirmPasswordVisibility() {
      this.showConfirmPassword = !this.showConfirmPassword;
    },
    toggleAdminUser() {
      this.isAdminUser = !this.isAdminUser;
    }
  }
};
</script>

<style scoped>
.signup-form {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20px;
    border: 2px solid rgba(255, 255, 255, 0.2);
    border-radius: 12px;
    width: 400px;
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(15px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    font-family: "Wix Madefor Display", sans-serif;
}

.form-title {
    margin-top: 70px;
    color: white;
    font-size: 36px;
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
.email-container,
.password-container {
    position: relative;
    width: 130%;
    color: white;
    font-size: 18px;
    font-family: "Wix Madefor Display", sans-serif;
}

.username-container input,
.email-container input,
.password-container input{
    color: white;
    font-size: 18px;
    font-family: "Wix Madefor Display", sans-serif;
}

.username-container, .email-container {
    margin-right: 15px;
}

.username-container input::placeholder {
    color: white;
    font-size: 18px;
}

.email-container input::placeholder {
    color: white;
    font-size: 18px;
}

.password-container input::placeholder {
    color: white;
    font-size: 18px;
}

.user-icon, .email-icon {
    position: relative;
    right: -25px;
    top: 35%;
    color: white;
    font-size: 18px;
    pointer-events: none;
}

.show-password-btn {
    position: absolute;
    left: 103px;
    top: 22%;
    background: none;
    border: none;
    color:white;
    cursor: pointer;
    font-size: 20px;
}

.padded-input {
    padding-left: 40px;
}

.button-group {
    width: 60%;
    display: flex;
    margin-top: 30px;
    flex-direction: column;
}

.accept-btn {
    padding: 10px 20px;
    border-radius: 20px;
    background-color: white;
    border: 2px solid white;
    margin-bottom: 5px;
    cursor: pointer;
    color: #333;
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
    padding: 10px 20px;
    border-radius: 20px;
    background-color: #333;
    border: 2px solid #333;
    margin-top: 5px;
    margin-bottom: 20px;
    cursor: pointer;
    color: white;
    font-size: 18px;
    font-family: "Wix Madefor Display", sans-serif;
}

.accept-btn:hover,
.login-btn:hover {
    opacity: 0.9;
}

.admin-toggle-container {
    margin-top: 20px;
    display: flex;
    flex-direction: column;
    align-items: center;
}

.admin-toggle-btn {
    background-color: transparent;
    border: 2px solid #D160DE;
    color: #D160DE;
    border-radius: 40px;
    padding: 12px 20px;
    font-size: 16px;
    font-weight: bold;
    font-family: "Wix Madefor Display", sans-serif;
}

.admin-status {
    margin-top: -10px;
    margin-bottom: 20px;
    color: #D160DE;
    font-size: 20px;
    font-family: "Wix Madefor Display", sans-serif;
}

</style>

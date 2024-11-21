<template>    
  <div class="signup-form">
    <h2 class="form-title">Sign Up</h2>
    
    <div class="username-container">
      <font-awesome-icon class="user-icon" :icon="['fas', 'user']" />
      <input
	v-model="username"
	type="text"
	id="username"
	placeholder="Your username"
	:class="{ 'input-error': usernameError, 'padded-input': true }"
	@input="validateUser" />
    </div>
    <span v-if="usernameError" class="error-message">{{ usernameError }}</span>
    
    <div class="email-container">
      <font-awesome-icon class="email-icon" :icon="['fas', 'envelope']" />
      <input
	v-model="email"
	type="email"
	id="email"
	placeholder="Your email"
	:class="{ 'input-error': emailError, 'padded-input': true }"
	@input="validateEmail" />
    </div>
    <span v-if="emailError" class="error-message">{{ emailError }}</span>
    
    <div class="password-container">
      <input
	v-model="password"
	:type="showPassword ? 'text' : 'password'"
	id="password"
	placeholder="Your password"
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
    <span v-if="passwordError" class="error-message">{{ passwordError }}</span>
    
    <div class="password-container">
      <input
	v-model="password2"
	:type="showConfirmPassword ? 'text': 'password'"
	id="password2"
	placeholder="Confirm your password"
	:class="{ 'input-error': confirmPasswordError, 'padded-input': true }"
	@input="clearError('password2')" />
    <button 
      type="button" 
      class="show-password-btn" 
      @click="toggleConfirmPasswordVisibility"
      aria-label="Show or Hide Confirm Password">
      <span :class="{ 'gg-eye': true, 'gg-eye-alt': showConfirmPassword }"></span>
    </button>
    </div>
    <span v-if="confirmPasswordError" class="error-message">{{ confirmPasswordError }}</span>
    
    <div class="button-group">
      <button class="accept-btn" @click="emitSignUp" >Create User</button>
      <button class="login-btn" @click="$emit('goToLogin')">Log In</button>
    </div>
  </div>
</template>

<script>
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import isEmail from "validator/lib/isEmail";

export default {
  name: "SignUpForm",
  components: {
    FontAwesomeIcon
  },
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
      showConfirmPassword: false
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
      else if (this.username.length < 3) this.usernameError = 'Username requieres at least 3 characters';
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
        this.$emit("signUp", { username: this.username, email: this.email, password: this.password, password2: this.password2});
      }
    },
    validateUsername() {
      this.usernameError = '';
      if (this.username.length > 0 && this.username.length < 3) {
        this.usernameError = 'Username must be at least 3 characters long';
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
    color: #e42121;
    font-size: 12px;
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
    margin-bottom: 15px;
    cursor: pointer;
    color: #333;
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

.accept-btn:hover,
.login-btn:hover {
    opacity: 0.9;
}
</style>

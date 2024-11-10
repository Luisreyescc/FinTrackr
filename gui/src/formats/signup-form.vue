<template>
<div class="signup-form">
  <h2 class="form-title">Sign Up</h2>
  
  <label for="username">Username</label>
  <div class="username-container">
    <span class="user-icon gg-user"></span>
    <input
      v-model="username"
      type="text"
      id="username"
      placeholder="Enter a username..."
      :class="{ 'input-error': usernameError, 'padded-input': true }"
      @input="validateUser"/>
  </div>
  <span v-if="usernameError" class="error-message">{{ usernameError }}</span>

    <label for="email">E-mail</label>
    <div class="email-container">
      <span class="email-icon gg-mail"></span>
      <input
        v-model="email"
        type="email"
        id="email"
        placeholder="Enter your email..."
        :class="{ 'input-error': emailError, 'padded-input': true }"
        @input="validateEmail"
      />
    </div>
  <span v-if="emailError" class="error-message">{{ emailError }}</span>
  
  <label for="password">Password</label>
  <div class="password-container">
    <input
      v-model="password"
      :type="showPassword ? 'text' : 'password'"
      id="password"
      placeholder="Insert a password..."
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
  
  <label for="conf_password">Confirm password</label>
  <div class="password-container">
    <input
      v-model="conf_password"
      :type="showConfirmPassword ? 'text': 'password'"
      id="conf_password"
      placeholder="Confirm your password..."
      :class="{ 'input-error': confirmPasswordError, 'padded-input': true }"
      @input="clearError('conf_password')"/>
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
import isEmail from "validator/lib/isEmail";
import '@/css/mail.css';

export default {
  name: 'SignUpForm',
  data() {
    return {
      username: '',
      email: '',
      password: '',
      conf_password: '',
      usernameError: '',
      emailError: '',
      passwordError: '',
      confirmPasswordError: '',
      showPassword: false,
      showConfirmPassword: false
    };
  },
  methods: {
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
      if (!this.conf_password)
	this.confirmPasswordError = 'Confirm password is required';
      if (this.password && this.conf_password && this.password !== this.conf_password) {
	this.passwordError = 'Passwords don\'t match';
	this.confirmPasswordError = 'Passwords don\'t match';
      }
      if (!this.usernameError && !this.emailError && !this.passwordError && !this.confirmPasswordError) {
	this.$emit('signUp', { username: this.username, email: this.email, password: this.password});
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
    clearError(field) {
      if (field === 'username')
	this.usernameError = '';
      if (field === 'email')
	this.emailError = '';
      if (field === 'password')
	this.passwordError = '';
      if (field === 'conf_password')
	this.confirmPasswordError = '';
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
/* Sign-up form styling */
.signup-form {
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

.button-group {
    width: 100%;
    display: flex;
    flex-direction: column;
}

.accept-btn {
    padding: 10px 20px;
    border: none;
    border-radius: 4px;
    font-size: 14px;
    cursor: pointer;
    background-color: #4CAF50;
    color: white;
    margin-bottom: 15px;
    font-family: "Wix Madefor Display", sans-serif;
}

.login-btn {
    padding: 10px 20px;
    border: none;
    border-radius: 4px;
    font-size: 14px;
    cursor: pointer;
    background-color: #333;
    color: white;
    font-family: "Wix Madefor Display", sans-serif;
}

.accept-btn:hover, .login-btn:hover {
    opacity: 0.9;
}

.username-container {
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

.email-container {
    display: flex;
    align-items: center;
    position: relative;
    width: 108%;
}

.email-icon {
    position: absolute;
    left: 13px;
    color: #555;
    font-size: 18px;
    margin-top: -5%;
    pointer-events: none;
}

.password-container {
    display: flex;
    align-items: center;
    position: relative;
    width: 108%;
}

.show-password-btn {
    position: absolute;
    padding-left: 10px;
    background: none;
    border: none;
    color: #555;
    cursor: pointer;
    font-size: 18px;
}

.show-password-btn span {
    font-size: 18px;
    display: flex;
    margin-top: -68%;
}

.padded-input {
  padding-left: 40px;
}

</style>

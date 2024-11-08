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
      @input="clearError('username')"/>
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
      @input="clearError('email')"/>
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
   
   <label for="conf_password">Confirm password</label>
   <div class="password-container">
     <input
       v-model="conf_password"
       type="password"
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
     <button class="login-btn" @click="$emit('goToLogin')">Log In</button>
     <button class="accept-btn" @click="emitSignUp" :disabled="isCreateUserDisabled">Create User</button>
  </div>
</div>
</template>

<script>
export default {
  name: 'SignUpForm',
  data() {
    return {
      username: '',
      email: '',
      password: '',
      conf_password: '',
      showPassword: false,
      showConfirmPassword: false,
      usernameError: '',
      emailError: '',
      passwordError: '',
      confirmPasswordError: ''
    };
  },
  computed: {
    // Computed property to check if any required fields are empty
    isCreateUserDisabled() {
      return !this.username || !this.email || !this.password || !this.conf_password || this.conf_password !== this.password;
    }
  },
  methods: {
    emitSignUp() {
      this.clearErrors();
      if (!this.username) this.usernameError = 'Username is required';
      if (!this.email) this.emailError = 'Email is required';
      if (!this.password) this.passwordError = 'Password is required';
      if (!this.conf_password) this.confirmPasswordError = 'Confirm password is required';
      if (this.password && this.conf_password && this.password !== this.conf_password) {
        this.confirmPasswordError = 'Passwords don\'t match';
      }
      if (!this.usernameError && !this.emailError && !this.passwordError && !this.confirmPasswordError) {
	this.$emit('signUp', { username: this.username, email: this.email, password: this.password});
	}
    },
    togglePasswordVisibility() {
      this.showPassword = !this.showPassword;
    },
    toggleConfirmPasswordVisibility() {
      this.showConfirmPassword = !this.showConfirmPassword;
    },
    clearError(field) {
      if (field === 'username') this.usernameError = '';
      if (field === 'email') this.emailError = '';
      if (field === 'password') this.passwordError = '';
      if (field === 'conf_password') this.confirmPasswordError = '';
    },
    clearErrors() {
      this.usernameError = '';
      this.emailError = '';
      this.passwordError = '';
      this.confirmPasswordError = '';
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

.padded-input {
  padding-left: 40px;
}

.button-group {
  display: flex;
  width: 100%;
  justify-content: space-between;
}

.accept-btn {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  background-color: #4CAF50;
  color: white;
}

.login-btn {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  background-color: #333;
  color: white;
  cursor: pointer;
}

.accept-btn:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.accept-btn:hover:not(:disabled), .login-btn:hover {
  opacity: 0.9;
}

username-container, .email-container, .password-container {
  display: flex;
  align-items: center;
  position: relative;
  width: 108%;
}

.user-icon, .email-icon {
  position: absolute;
  left: 15px;
  color: #555;
  font-size: 18px;
  pointer-events: none;
}

.show-password-btn {
  position: absolute;
  right: 10px;
  background: none;
  border: none;
  color: #555;
  cursor: pointer;
  font-size: 18px;
}

.show-password-btn span {
  font-size: 18px;
  display: flex;
}
</style>

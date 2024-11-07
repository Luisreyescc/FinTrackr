<template>
<div class="login-form">
  <h2 class="form-title">Log In</h2>

  <label for="username">Username</label>
  <input
    v-model="username" 
    type="text" 
    id="username" 
    placeholder="Insert username..."
    :class="{ 'input-error': usernameError }"
    @input="clearError('username')"/>
  
  <span v-if="usernameError" class="error-message">{{ usernameError }}</span>
  <label for="password">Password</label>
  <div class="password-container">
    <input 
      v-model="password" 
      :type="showPassword ? 'text': 'password'" 
      id="password" 
      placeholder="Insert the password.."
      :class="{ 'input-error': passwordError }" 
      @input="clearError('password')" 
    />
    
    <button 
      type="button" 
      class="show-password-btn" 
      @click="togglePasswordVisibility"
      aria-label="Show or Hide Password"
    >
      <span :class="{ 'gg-eye': true, 'gg-eye-alt': showPassword }"></span>
    </button>
  </div>

  <span v-if="passwordError" class="error-message">{{ passwordError }}</span>

  <!-- Buttons -->
  <div class="button-group">
    <button class="sign-in-btn" @click="emitLogin">Sign-in</button>
    <button class="register-btn" @click="$emit('goToSignUp')">Sing-up</button>
  </div>
  
    <!-- Recover Password Link -->
  <a href="#" class="recover-password" @click.prevent="goToRecovery">Forget password?</a>
</div>
</template>

<script>
import '@/css/eye.css';
import '@/css/eye-alt.css';
import '@/css/user.css';
export default {
  name: 'LoginForm',
  data() {
    return {
      username: '',
      password: '',
      usernameError: '',
      passwordError: '',
      showPassword: false
    };
  },
  methods: {
    emitLogin() {
      // Clean previous errors
      this.usernameError = '';
      this.passwordError = '';
      if (!this.username) this.usernameError = 'Username is required';
      if (!this.password) this.passwordError = 'Password is required';
      if(!this.usernameError && this.passwordError){
        // Emit an event with username and password data to the parent
        this.$emit('login', { username: this.username, password: this.password });
      }
    },
    clearError(field) {
      if (field === 'username') this.usernameError = '';
      if (field === 'password') this.passwordError = '';
    },
    togglePasswordVisibility(){
      this.showPassword = !this.showPassword;
      console.log(this.password);
    },
    goToRecovery() {
      // Emit an event to navigate to the recovery page
      this.$emit('goToRecovery');
    }
  }
};
</script>

<style scoped>
/* Login form styling */
.login-form {
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

.input-error{
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

/* .sign-in-btn, .register-btn {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  font-family: "Wix Madefor Display", sans-serif;
} */

.sign-in-btn {
    padding: 10px 20px;
    border: none;
    border-radius: 4px;
    font-size: 14px;
    background-color: #4CAF50;
    color: white;
    margin-bottom: 15px;
    font-family: "Wix Madefor Display", sans-serif;
}

.register-btn {
    padding: 10px 20px;
    border: none;
    border-radius: 4px;
    font-size: 14px;
    cursor: pointer;
    background-color: #333;
    color: white;
    font-family: "Wix Madefor Display", sans-serif;
}

.sign-in-btn:hover, .register-btn:hover {
  opacity: 0.9;
}

.recover-password {
  margin-top: 15px;
  font-size: 14px;
  color: #555;
  text-decoration: none;
  font-family: "Wix Madefor Display", sans-serif;
}

.password-container {
  display: flex;
  align-items: center;
  position: relative;
  width: 108%;
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
  margin-top: -58%;
}

.recover-password:hover {
  text-decoration: underline;
}

</style>

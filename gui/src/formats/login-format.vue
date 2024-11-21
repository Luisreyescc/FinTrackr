<template>
<div class="login-form">
  <h2 class="form-title">Log In</h2>
  
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
  <span v-if="usernameError" class="error-message">{{ usernameError }}</span>
  
  <div class="password-container">
    <input
      v-model="password"
      :type="showPassword ? 'text' : 'password'"
      id="password"
      placeholder="Password"
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
  
  <div class="button-group">
    <button class="sign-in-btn" @click="emitLogin">Log-in</button>
    <button class="register-btn" @click="$emit('goToSignUp')">Sing-up</button>
  </div>
  
  <a href="#" class="recover-password" @click.prevent="goToRecovery"> Forget password?</a>
</div>
</template>

<script>
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import "@/css/eye.css";
import "@/css/eye-alt.css";

export default {
  name: "LoginForm",
  components: { FontAwesomeIcon },
  data() {
    return {
      username: "",
      password: "",
      usernameError: "",
      passwordError: "",
      showPassword: false
    };
  },
  methods: {
    clearError(field) {
      if (field === 'username')
	this.usernameError = false;
      if (field === 'password')
	this.passwordError = false;
    },
    emitLogin() {
      this.usernameError = "";
      this.passwordError = "";
      if (!this.username)
	this.usernameError = "Username is required";
      if (!this.password)
	this.passwordError = "Password is required";
      if (!this.usernameError && !this.passwordError) {
        // Emit an event with username and password data to the parent
        this.$emit("login", {
          username: this.username,
          password: this.password,
        });
      }
    },
    togglePasswordVisibility() {
      this.showPassword = !this.showPassword;
      console.log(this.password);
    },
    goToRecovery() {
      this.$emit("goToRecovery");
    },
  },
};
</script>

<style scoped>
.login-form {
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

.username-container, .password-container {
    position: relative;
    width: 130%;
    color: white;
    font-size: 18px;
    font-family: "Wix Madefor Display", sans-serif;
}

.username-container input, .password-container input{
    color: white;
    font-size: 18px;
    font-family: "Wix Madefor Display", sans-serif;
}

.username-container {
    margin-right: 15px;
}

.username-container input::placeholder {
    color: white;
    font-size: 18px;
}

.password-container input::placeholder {
    color: white;
    font-size: 18px;
}

.user-icon {
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

.sign-in-btn {
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

.register-btn {
    padding: 10px 20px;
    border-radius: 20px;
    background-color: #333;
    border: 2px solid #333;
    margin-top: 20px;
    cursor: pointer;
    color: white;
    font-size: 18px;
    font-family: "Wix Madefor Display", sans-serif;
}

.sign-in-btn:hover,
.register-btn:hover {
    opacity: 0.9;
}

.recover-password {
    margin-top: 35px;
    font-size: 16px;
    color: white;
    text-decoration: none;
    font-family: "Wix Madefor Display", sans-serif;
}

.recover-password:hover {
    text-decoration: underline;
}

.message-container {
    width: 100%;
    max-width: 400px;
    position: absolute;
}
</style>

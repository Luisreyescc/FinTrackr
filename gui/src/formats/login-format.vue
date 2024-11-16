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

    <div class="button-group">
      <button class="sign-in-btn" @click="emitLogin">Sign-in</button>
      <button class="register-btn" @click="$emit('goToSignUp')">Sing-up</button>
    </div>
  
    <a href="#" class="recover-password" @click.prevent="goToRecovery"> Forget password?</a>
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
import "@/css/eye.css";
import "@/css/eye-alt.css";

export default {
  name: "LoginForm",
  components: { FontAwesomeIcon, MessageAlerts },
  data() {
    return {
      username: "",
      password: "",
      usernameError: false,
      passwordError: false,
      showPassword: false,
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
      if (field === 'username') this.usernameError = false;
      if (field === 'password') this.passwordError = false;
    },
    emitLogin() {
      if (this.validateInputs()) {
        // Emit an event with username and password data to the parent
        this.$emit("login", {
          username: this.username,
          password: this.password,
        });
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
      if (!this.password) {
        this.addMessage("Password is required.", "error");
        this.passwordError = true;
        isValid = false;
      }
      
      return isValid;
    },
    togglePasswordVisibility() {
      this.showPassword = !this.showPassword;
      console.log(this.password);
    },
    goToRecovery() {
      // Emit an event to navigate to the recovery page
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
    color: #333;
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

<template>
<div class="login-form">
  <h2 class="form-title">Log In</h2>
  <label for="username">Username</label>
  <input v-model="username" type="text" id="username" placeholder="Insert username..." />
  
  <label for="password">Password</label>
  <input v-model="password" type="password" id="password" placeholder="Insert the password.." />
  
  <!-- Buttons -->
  <div class="button-group">
    <button class="sign-in-btn" @click="emitLogin">Sign-in</button>
    <button class="register-btn" @click="$emit('goToSignUp')">Sing-up</button>
  </div>
  
    <!-- Recover Password Link -->
  <a href="#" class="recover-password" @click.prevent="goToRecovery">Recover password</a>
</div>
</template>

<script>
export default {
  name: 'LoginForm',
  data() {
    return {
      username: '',
      password: ''
    };
  },
  methods: {
    emitLogin() {
      // Emit an event with username and password data to the parent
      this.$emit('login', { username: this.username, password: this.password });
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
}

label {
  align-self: flex-start;
  margin-bottom: 5px;
  font-weight: bold;
  color: #333;
}

input {
  width: 100%;
  padding: 10px;
  margin-bottom: 15px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  color: #333;
}

.button-group {
  display: flex;
  width: 100%;
  justify-content: space-between;
}

.sign-in-btn, .register-btn {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
}

.sign-in-btn {
  background-color: #f0f0f0;
  color: #333;
}

.register-btn {
  background-color: #333;
  color: white;
}

.sign-in-btn:hover, .register-btn:hover {
  opacity: 0.9;
}

.recover-password {
  margin-top: 15px;
  font-size: 14px;
  color: #555;
  text-decoration: none;
}

.recover-password:hover {
  text-decoration: underline;
}
</style>

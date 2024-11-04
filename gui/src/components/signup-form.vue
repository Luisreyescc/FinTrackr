<template>
  <div class="signup-form">
    <label for="username">Username</label>
    <input v-model="username" type="text" id="username" placeholder="Insert a username..." />
    <label for="email">Email</label>
    <input v-model="email" type="email" id="email" placeholder="Insert your email..." />
    <label for="password">Password</label>
    <input v-model="password" type="password" id="password" placeholder="Insert a password..." />
    
    <div class="button-group">
      <button class="login-btn" @click="$emit('goToLogin')">Log In</button>
      <button class="accept-btn" @click="emitSignUp">Create User</button>
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
      password: ''
    };
  },
  methods: {
    emitSignUp() {
      this.$emit('signUp', { username: this.username, email: this.email, password: this.password });
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

.accept-btn, .login-btn {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
}

.login-btn {
  background-color: #f0f0f0;
  color: #333;
}

.accept-btn {
  background-color: #333;
  color: white;
}

.accept-btn:hover, .login-btn:hover {
  opacity: 0.9;
}
</style>

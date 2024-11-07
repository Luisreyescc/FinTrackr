<template>
<div class="signup-form">
  <h2 class="form-title">Sign Up</h2>
  <label for="username">Username</label>
  <input v-model="username" type="text" id="username" placeholder="Enter a username..." />
  <label for="email">E-mail</label>
  <input v-model="email" type="email" id="email" placeholder="Enter your email..." />
  
  <label for="name">Name(s)</label>
  <input v-model="name" type="text" id="name" placeholder="Enter your name or names..." />
  <label for="lastName">Last Name(s)</label>
  <input v-model="lastName" type="text" id="lastName" placeholder="Enter your last name..." />
  <label for="phone">Phone Number</label>
  <input v-model="phone" type="tel" id="phone" placeholder="Enter your phone number..." />
  <label for="curp">CURP</label>
  <input v-model="curp" type="text" id="curp" placeholder="Enter your CURP..." />
  <label for="rfc">RFC</label>
  <input v-model="rfc" type="text" id="rfc" placeholder="Enter your RFC..." />
  <label for="birthDate">Date of Birth</label>
  <input v-model="birthDate" type="date" id="birthDate" />
  
  <label for="password">Password</label>
  <input v-model="password" type="password" id="password" placeholder="Insert a password..." />
  <label for="conf_password">Confirm password</label>
  <input v-model="conf_password" type="password" id="conf_password" placeholder="Confirm your password..." />
  
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
      name: '',
      lastName: '',
      phone: '',
      curp: '',
      rfc: '',
      birthDate: '',
      password: '',
      conf_password: ''
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
      this.$emit('signUp', { username: this.username, email: this.email, password: this.password});
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
  font-family: "Wix Madefor Display", sans-serif;
}

.login-btn {
  background-color: #f0f0f0;
  color: #333;
}

.accept-btn {
  background-color: #333;
  color: white;
}

.accept-btn:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.accept-btn:hover:not(:disabled), .login-btn:hover {
  opacity: 0.9;
}
</style>

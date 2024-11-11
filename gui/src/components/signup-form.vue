<template>
  <div class="form-container">
    <h2>Sign Up</h2>
    <form @submit.prevent="submitForm">
      <label for="username">Username</label>
      <input
        v-model="username"
        type="text"
        id="username"
        placeholder="Enter your username"
        @input="clearError('username')"
      />
      <span v-if="usernameError" class="error-message">{{
        usernameError
      }}</span>

      <label for="email">Email</label>
      <input
        v-model="email"
        type="email"
        id="email"
        placeholder="Enter your email"
        @input="clearError('email')"
      />
      <span v-if="emailError" class="error-message">{{ emailError }}</span>

      <label for="password">Password</label>
      <input
        v-model="password"
        type="password"
        id="password"
        placeholder="Enter your password"
        @input="clearError('password')"
      />
      <span v-if="passwordError" class="error-message">{{
        passwordError
      }}</span>

      <label for="password2">Confirm Password</label>
      <input
        v-model="password2"
        type="password"
        id="password2"
        placeholder="Confirm your password"
        @input="clearError('password2')"
      />
      <span v-if="confirmPasswordError" class="error-message">{{
        confirmPasswordError
      }}</span>

      <button type="submit">Register</button>
    </form>
  </div>
</template>

<script>
export default {
  name: "SignUpForm",
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
    };
  },
  methods: {
    submitForm() {
      this.usernameError = "";
      this.emailError = "";
      this.passwordError = "";
      this.confirmPasswordError = "";

      if (!this.username) this.usernameError = "Username is required";
      if (!this.email) this.emailError = "Email is required";
      if (!this.password) this.passwordError = "Password is required";
      if (this.password !== this.password2) {
        this.confirmPasswordError = "Passwords don't match";
      }

      if (
        !this.usernameError &&
        !this.emailError &&
        !this.passwordError &&
        !this.confirmPasswordError
      ) {
        this.$emit("signUp", {
          username: this.username,
          email: this.email,
          password: this.password,
          password2: this.password2,
        });
      }
    },
    clearError(field) {
      if (field === "username") this.usernameError = "";
      if (field === "email") this.emailError = "";
      if (field === "password") this.passwordError = "";
      if (field === "password2") this.confirmPasswordError = "";
    },
  },
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
  border-color: #e42121;
}

.error-message {
  color: #e42121;
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
  background-color: #4caf50;
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

.accept-btn:hover,
.login-btn:hover {
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

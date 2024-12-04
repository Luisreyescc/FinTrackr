<template>
<div class="edit-form scrollbar">
  <div class="header">
    <h2 class="form-title">Edit Profile</h2>
    <img src="@/assets/profile_white.svg" alt="Profile Icon" class="profile-icon"/>
  </div>
  
  <div class="username-container">
    <font-awesome-icon class="user-icon" :icon="['fas', 'user']"/>
    <input
      v-model="formData.user_name"
      type="text"
      id="user_name"
      placeholder="Username"
      :class="{ 'input-error': usernameError, 'padded-input': true }"
      @input="validateUser"/>
  </div>
  <span v-if="usernameError" class="error-message">{{ usernameError }}</span>
  
  <div class="row">
    <div class="column">
      <div class="name-container">
	<font-awesome-icon class="name-icon" :icon="['fas', 'id-card']"/>
        <input v-model="formData.name" type="text" id="name" placeholder="Your name"/>
      </div>
    </div>
    <div class="column">
      <div class="last-name-container">
	<font-awesome-icon class="name-icon" :icon="['fas', 'id-card']"/>
        <input v-model="formData.last_name" type="text" id="last_name" placeholder="Your last name"/>
      </div>
    </div>
  </div>
  
  <div class="email-container">
    <font-awesome-icon class="email-icon" :icon="['fas', 'envelope']"/>
    <input
      v-model="formData.email"
      type="email"
      id="email"
      placeholder="Your email"
      :class="{ 'input-error': emailError, 'padded-input': true }"
      @input="validateEmail"/>
  </div>
  <span v-if="emailError" class="error-message">{{ emailError }}</span>
  
  <div class="curp-container">
    <font-awesome-icon class="curp-icon" :icon="['fas', 'passport']"/>
    <input
      v-model="formData.curp"
      type="text"
      id="curp"
      placeholder="Your Curp"
      :class="{ 'input-error': curpError }"
      @input="handleCurpInput"/>
  </div>
  <span v-if="curpError" class="error-message">{{ curpError }}</span>
  
  <div class="rfc-container">
    <font-awesome-icon class="rfc-icon" :icon="['fas', 'passport']"/>
    <input
      v-model="formData.rfc"
      type="text"
      id="rfc"
      placeholder="Your Rfc"
      :class="{ 'input-error': rfcError }"
      @input="handleRfcInput">
  </div>
  <span v-if="rfcError" class="error-message">{{ rfcError }}</span>
  
  <div class="row">
    <div class="column">
      <div class="phone-container">
        <font-awesome-icon class="phone-icon" :icon="['fas', 'plus']"/>
        <input
          v-model="formData.phone"
          type="tel"
          id="phone"
          placeholder="Your phone number"
          :class="{ 'input-error': phoneError, 'padded-input': true }"
          @input="validatePhone"/>
      </div>
      <span v-if="phoneError" class="error-message">{{ phoneError }}</span>
    </div>
    <div class="column">
      <div class="birth-container">
	<font-awesome-icon class="birth-icon" :icon="['fas', 'cake-candles']"/>
        <input v-model="formData.birth_date" type="date" id="birth_date"/>
      </div>
    </div>
  </div>
  
  <div class="password-container">
    <input
      v-model="formData.password"
      :type="showPassword ? 'text' : 'password'"
      id="password"
      placeholder="Your current password"
      class="padded-input"
      :class="{ 'input-error': passwordError, 'padded-input': true }"
      @input="clearError('password')"/>
    <button
      type="button"
      class="show-password-btn"
      @click="togglePasswordVisibility">
      <span :class="{ 'gg-eye': true, 'gg-eye-alt': showPassword }"></span>
    </button>
    <button
      type="button"
      :class="['change-password-btn', { 'close-btn': showPasswordFields }]"
      @click="togglePasswordFields">
      <span v-if="showPasswordFields"><font-awesome-icon :icon="['fas', 'xmark']" class="close-button"/></span>
      <span v-else>Change Password</span>
    </button>
  </div>
  <span v-if="passwordError" class="error-message">{{ passwordError }}</span>
  
  <div v-if="showPasswordFields">
    <div class="password-container">
      <input
        v-model="formData.newPassword"
        :type="showNewPassword ? 'text' : 'password'"
        id="new_password"
        placeholder="New password"
        :class="{ 'input-error': newPasswordError }"
	@input="clearError('newPassword')"/>
      <button
        type="button"
        class="show-password-btn"
        @click="toggleNewPasswordVisibility" >
        <span :class="{ 'gg-eye': true, 'gg-eye-alt': showNewPassword }"></span>
      </button>
    </div>
    <span v-if="newPasswordError" class="error-message">{{ newPasswordError }}</span>
    
    <div class="password-container">
      <input
        v-model="formData.confirmPassword"
        :type="showConfirmPassword ? 'text' : 'password'"
        id="confirm_password"
        placeholder="Confirm new password"
        :class="{ 'input-error': confirmPasswordError }"
	@input="clearError('confirmPassword')"/>
      <button
        type="button"
        class="show-password-btn"
        @click="toggleConfirmPasswordVisibility">
        <span :class="{ 'gg-eye': true, 'gg-eye-alt': showConfirmPassword }"></span>
      </button>
    </div>
    <span v-if="confirmPasswordError" class="error-message">{{ confirmPasswordError }}</span>
  </div>
  
  <div class="button-group">
    <button class="cancel-btn" @click="$emit('goToHome')">Cancel</button>
    <button class="save-btn" @click="saveProfile">Save Changes</button>
  </div>
</div>
</template>

<script>
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import isEmail from "validator/lib/isEmail";

export default {
  name: "EditProfileForm",
  components: { FontAwesomeIcon },
  props: {
    initialData: {
      type: Object,
      default: () => ({})
    },
  },
  data() {
    return {
      formData: {
        user_name: this.initialData.user_name || "",
        name: this.initialData.name || "",
        last_name: this.initialData.last_name || "",
        email: this.initialData.email || "",
        curp: this.initialData.curp || "",
        rfc: this.initialData.rfc || "",
        phone: this.initialData.phone || "",
        birth_date: this.initialData.birth_date || "",
        password: "",
        new_password: "",
        confirm_password: ""
      },
      showPassword: false,
      showNewPassword: false,
      showConfirmPassword: false,
      showPasswordFields: false,
      usernameError: "",
      emailError: "",
      curpError: "",
      rfcError: "",
      phoneError: "",
      passwordError: "",
      newPasswordError: "",
      confirmPasswordError: ""
    };
  },
  watch: {
    initialData: {
      handler(newVal) {
        this.formData = {
          ...this.formData,
          user_name: newVal.user_name || "",
          name: newVal.name || "",
          last_name: newVal.last_name || "",
          email: newVal.email || "",
          curp: newVal.curp || "",
          rfc: newVal.rfc || "",
          phone: newVal.phone || "",
          birth_date: newVal.birth_date || "",
          password: "",
          new_password: "",
          confirm_password: ""
        };
      },
      deep: true,
      immediate: true
    },
  },
  methods: {
    validateUser() {
      this.usernameError = "";
      if (!this.formData.user_name)
	this.usernameError = "Username is required";
      else if (this.formData.user_name.length < 3 || this.formData.user_name.length > 16)
	this.usernameError = "Username must be between 3 and 16 characters";
    },
    validateEmail() {
      this.emailError = "";
      if (!this.formData.email)
	this.emailError = "Email is required";
      else if (!isEmail(this.formData.email))
	this.emailError = "Invalid email format";
    },
    validatePhone() {
      this.phoneError = "";
      if (this.formData.phone && !/^\d+$/.test(this.formData.phone))
	this.phoneError = "Only digits accepted";
    },
    validateChanges() {
      this.passwordError = "";
      if (!this.formData.password)
	this.passwordError = "Your current password is required to save changes.";
    },
    validatePasswords() {
      this.newPasswordError = "";
      this.confirmPasswordError = "";
      
      if (this.showPasswordFields) {
	if (!this.formData.newPassword)
	this.newPasswordError = "New password is required.";
	if (!this.formData.confirmPassword)
	this.confirmPasswordError = "Confirm password is required.";
	if (this.formData.newPassword
            && this.formData.confirmPassword
            && this.formData.newPassword
            !== this.formData.confirmPassword) {
	this.newPasswordError = "Passwords don't match.";
	this.confirmPasswordError = "Passwords don't match.";
	}
      }
    },
    handleCurpInput(event) {
      const curp = event.target.value.toUpperCase();
      this.curpError = "";
      if (curp.length > 18)
	this.curpError = "CURP can't have more than 18 characters";
      this.formData.curp = curp;
    },
    handleRfcInput(event) {
      const rfc = event.target.value.toUpperCase();
      this.rfcError = "";
      if (rfc.length > 13)
	this.rfcError = "RFC can't have more than 13 characters";
      this.formData.rfc = rfc;
    },
    clearError(field) {
      this[`${field}Error`] = "";
    },
    togglePasswordVisibility() {
      this.showPassword = !this.showPassword;
    },
    toggleNewPasswordVisibility() {
      this.showNewPassword = !this.showNewPassword;
    },
    toggleConfirmPasswordVisibility() {
      this.showConfirmPassword = !this.showConfirmPassword;
    },
    togglePasswordFields() {
      this.showPasswordFields = !this.showPasswordFields;
      if (!this.showPasswordFields) {
        this.formData.newPassword = "";
        this.formData.confirmPassword = "";
      }
    },
    saveProfile() {
      this.validateChanges();
      this.validateUser();
      this.validateEmail();
      this.validatePhone();
      this.validatePasswords();

      if (this.passwordError || this.usernameError
          || this.emailError ||  this.curpError
          || this.rfcError ||this.phoneError
          || this.newPasswordError || this.confirmPasswordError)
	return;
      
      const sanitizedData = Object.fromEntries(
        Object.entries(this.formData).map(([key, value]) => [key, value || null ]),
      );
      this.$emit("saveProfile", sanitizedData);
    },
    goToHome() {
      this.$emit("goToHome");
    }
  },
};
</script>

<style scoped>
.edit-form {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20px;
    margin-top: 50px;
    height: 100%;
    max-height: 80vh;
    overflow-y: auto;
    overflow-x: hidden;
    border: 2px solid rgba(255, 255, 255, 0.2);
    border-radius: 12px;
    width: 700px;
    background: #25262B;
    backdrop-filter: blur(15px);
    box-shadow: 0 2px 10px rgba(255, 255, 255, 0.2);
    font-family: "Wix Madefor Display", sans-serif;
}

.header {
    display: flex;
    align-items: center;
}

.form-title {
    font-size: 32px;
    font-weight: bold;
    color: white;
    font-family: "Wix Madefor Display", sans-serif;
}

.profile-icon {
    width: 90px;
    height: 90px;
    margin-left: 400px;
    border-radius: 50%;
    border: 2px solid white;
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(5px);
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

.username-container,
.email-container,
.curp-container,
.rfc-container {
    align-items: center;
    position: relative;
    margin-right: 20px;
    width: 150%;
    color: white;
    font-size: 18px;
    font-family: "Wix Madefor Display", sans-serif;
}

.name-container,
.last-name-container,
.phone-container,
.birth-container {
    align-items: center;
    position: relative;
    width: 130%;
    color: white;
    font-size: 18px;
    font-family: "Wix Madefor Display", sans-serif;
}

.password-container {
    display: flex;
    align-items: center;
    position: relative;
    justify-content: space-between;
    width: 100%;
    color: white;
    font-size: 18px;
    margin-bottom: 20px;
    font-family: "Wix Madefor Display", sans-serif;
}

.username-container input,
.email-container input {
    color: white;
    font-size: 18px;
    font-family: "Wix Madefor Display", sans-serif;
}

.name-container input,
.last-name-container input,
.curp-container input,
.rfc-container input,
.phone-container input {
    padding-left: 40px;
    color: white;
    font-size: 18px;
    font-family: "Wix Madefor Display", sans-serif;
}

.birth-container input {
    color: white;
    font-size: 18px;
    font-family: "Wix Madefor Display", sans-serif;
}

.password-container input {
    flex: 1;
    padding-left: 40px;
    padding-right: 40px;
    color: white;
    font-size: 18px;
    font-family: "Wix Madefor Display", sans-serif;
}

.username-container input::placeholder {
    color: white;
    font-size: 18px;
}

.name-container input::placeholder {
    color: white;
    font-size: 18px;
}

.last-name-container input::placeholder {
    color: white;
    font-size: 18px;
}

.curp-container input::placeholder {
    color: white;
    font-size: 18px;
}

.rfc-container input::placeholder {
    color: white;
    font-size: 18px;
}

.email-container input::placeholder {
    color: white;
    font-size: 18px;
}

.phone-container input::placeholder {
    color: white;
    font-size: 18px;
}

.birth-container input::placeholder {
    color: white;
    font-size: 18px;
}

.password-container input::placeholder {
    color: white;
    font-size: 18px;
}

.row {
    display: flex;
    width: 100%;
    gap: 10px;
    margin-left: -80px;
}

.column {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
}

.user-icon,
.name-icon,
.email-icon,
.curp-icon,
.rfc-icon,
.phone-icon {
    margin-right: -25px;
    font-size: 22px;
    color: white;
}

.padded-input {
    padding-left: 40px;
}

.birth-container input {
    padding-left: 2px;
}

.button-group {
    display: flex;
    width: 100%;
    justify-content: space-between;
}

.birth-icon {
    margin-right: -25px;
    transform: translateX(1040%);
    font-size: 22px;
    color: white;
}

.save-btn,
.cancel-btn,
.change-password-btn {
    color: white;
    border: none;
    padding: 15px 40px;
    border-radius: 20px;
    cursor: pointer;
    font-size: 16px;
    font-weight: bold;
    font-family: "Wix Madefor Display", sans-serif;
    transition: background-color 0.3s ease, transform 0.2s ease;
}

.save-btn {
    background-color: white;
    border: 2px solid white;
    color: #25262B;
}

.cancel-btn {
    background-color:  #25262B;
    border: 2px solid  white;
    color: white;
}

.show-password-btn {
    position: absolute;
    left: 2px;
    top: 35%;
    transform: translateY(-50%);
    background: none;
    border: none;
    color: white;
    cursor: pointer;
    font-size: 20px;
}

.change-password-btn {
    margin-left: 20px;
    margin-top: 20px;
    margin-bottom: 20px;
    background-color: #25262B;
    border: 2px solid #BF9F00;
    color: #BF9F00;
    border-radius: 20px;
    padding: 12px 20px;
    font-size: 16px;
    font-weight: bold;
}

.save-btn:hover,
.cancel-btn:hover,
.change-password-btn:hover {
    opacity: 0.9;
}

.change-password-btn.close-btn {
    background-color: #e53935;
    border: 2px solid #e53935;
    border-radius: 3px;
    color: white;
    padding: 3px 8px;
    font-size: 22px;
    width: auto;
}

.password-input-wrapper {
    position: relative;
    width: 70%;
}

.birth-container input[type="date"]::-webkit-calendar-picker-indicator {
    opacity: 0;
    cursor: pointer;
}
</style>

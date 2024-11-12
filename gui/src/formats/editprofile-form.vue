<template>
<div class="edit-form">
  <div class="title-container">
    <h2 class="form-title">Edit Profile</h2>
    <img src="@/assets/profile_black.svg" alt="Profile Icon" class="profile-icon" />
  </div>
  
  <label for="username">Username</label>
  <div class="username-container">
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512" class="user-icon" >
      <path d="M224 256A128 128 0 1 0 224 0a128 128 0 1 0 0 256zm-45.7 48C79.8 304 0 383.8 0 482.3C0 498.7 13.3 512 29.7 512l388.6 0c16.4 0 29.7-13.3 29.7-29.7C448 383.8 368.2 304 269.7 304l-91.4 0z"/>
    </svg>
    <input
      v-model="formData.username"
      type="text"
      id="username"
      placeholder="Enter a username..."
      :class="{ 'input-error': usernameError, 'padded-input': true }"
      @input="validateUser" />
  </div>
  <span v-if="usernameError" class="error-message">{{ usernameError }}</span>
  
  <div class="row">
    <div class="column">
      <label for="name">Name(s)</label>
      <input
        v-model="formData.name"
        type="text"
        id="name"
        placeholder="Enter your name or names..." />
    </div>
    <div class="column">
      <label for="lastName">Last Name(s)</label>
      <input
        v-model="formData.lastName"
        type="text"
        id="lastName"
        placeholder="Enter your last name..." />
    </div>
  </div>
  
  <label for="email">E-mail</label>
  <div class="email-container">
    <span class="email-icon gg-mail"></span>
    <input
      v-model="formData.email"
      type="email"
      id="email"
      placeholder="Enter your email..."
      :class="{ 'input-error': emailError, 'padded-input': true }"
      @input="validateEmail" />
  </div>
  <span v-if="emailError" class="error-message">{{ emailError }}</span>
  
  <label for="curp">CURP</label>
  <input
    v-model="formData.curp"
    type="text"
    id="curp"
    placeholder="Enter your CURP..." />
  
  <label for="rfc">RFC</label>
  <input
    v-model="formData.rfc"
    type="text"
    id="rfc"
    placeholder="Enter your RFC..." />
  
  <div class="row">
    <div class="column">
      <label for="phone">Phone Number</label>
      <div class="phone-container">
	<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"  class="phone-icon" >
	<path d="M256 80c0-17.7-14.3-32-32-32s-32 14.3-32 32l0 144L48 224c-17.7 0-32 14.3-32 32s14.3 32 32 32l144 0 0 144c0 17.7 14.3 32 32 32s32-14.3 32-32l0-144 144 0c17.7 0 32-14.3 32-32s-14.3-32-32-32l-144 0 0-144z" />
	</svg>
	<input v-model="formData.phone" type="tel" id="phone" placeholder="Enter your phone number..." :class="{ 'input-error': phoneError, 'padded-input': true }" @input="validatePhone" />
      </div>
      <span v-if="phoneError" class="error-message">{{ phoneError }}</span>
    </div>
    
    <div class="column">
      <label for="birthDate">Date of Birth</label>
      <input v-model="formData.birthDate" type="date" id="birthDate" />
    </div>
  </div>
  
  <label for="password">Current Password</label>
  <div class="password-container">
    <input
      v-model="formData.password"
      :type="showPassword ? 'text' : 'password'"
      id="password" />
    <button
      type="button"
      class="show-password-btn"
      @click="togglePasswordVisibility" >
      <span :class="{ 'gg-eye': true, 'gg-eye-alt': showPassword }"></span>
    </button>
    <button type="button" class="change-password-btn" @click="togglePasswordFields">
      {{ showPasswordFields ? "Close" : "Change Password" }}
    </button>
  </div>

  <div v-if="showPasswordFields">
    <label for="new_password">New Password</label>
    <div class="password-container">
      <input
        v-model="formData.newPassword"
        :type="showNewPassword ? 'text' : 'password'"
        id="new_password"
        placeholder="Enter a new password..." />
      <button type="button" class="show-password-btn" @click="toggleNewPasswordVisibility">
        <span :class="{ 'gg-eye': true, 'gg-eye-alt': showNewPassword }"></span>
      </button>
    </div>
    
    <label for="confirm_password">Confirm New Password</label>
    <div class="password-container">
      <input
        v-model="formData.confirmPassword"
        :type="showConfirmPassword ? 'text' : 'password'"
        id="confirm_password"
        placeholder="Confirm new password..." />
      <button type="button" class="show-password-btn" @click="toggleConfirmPasswordVisibility">
        <span :class="{ 'gg-eye': true, 'gg-eye-alt': showConfirmPassword }"></span>
      </button>
    </div>
  </div>
  
  <div class="button-group">
    <button class="cancel-btn" @click="$emit('goToHome')">Cancel</button>
    <button class="save-btn" @click="saveProfile">Save Changes</button>
  </div>
</div>
</template>

<script>
import isEmail from "validator/lib/isEmail";
  
export default {
  name: "EditProfileForm",
  props: {
    initialData: {
      type: Object,
      default: () => ({}),
    },
  },
  data() {
    return {
      formData: {
        username: this.initialData.username || "",
        name: this.initialData.name || "",
        lastName: this.initialData.lastName || "",
        email: this.initialData.email || "",
        curp: this.initialData.curp || "",
        rfc: this.initialData.rfc || "",
        phone: this.initialData.phone || "",
        birthDate: this.initialData.birthDate || "",
        password: this.initialData.password || "",
	newPassword: "",
        confirmPassword: "",
      },
      showCurrentPassword: false,
      showNewPassword: false,
      showConfirmPassword: false,
      showPasswordFields: false,
      usernameError: "",
      emailError: "",
      phoneError: "",
    };
  },
  methods: {
    validateUsername() {
      this.usernameError = this.formData.username
        ? this.formData.username.length >= 3
          ? ""
          : "Username must be at least 3 characters."
        : "Username is required.";
    },
    validateEmail() {
      this.emailError = this.formData.email
        ? isEmail(this.formData.email)
          ? ""
          : "Invalid email format."
        : "Email is required.";
    },
    validatePhone() {
      this.phoneError = this.formData.phone && !/^\d+$/.test(this.formData.phone)
        ? "Phone number must be numeric."
        : "";
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
      this.validateUsername();
      this.validateEmail();
      this.validatePhone();
      
      const sanitizedData = Object.fromEntries(
        Object.entries(this.formData).map(([key, value]) => [
          key,
          value || null,
        ]),
      );
      this.$emit("saveProfile", sanitizedData);
    },
    goToHome() {
      this.$emit("goToHome");
    }
  }
};
</script>

<style scoped>
.edit-form {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20px;
    margin: 0 auto;
    border: 1px solid #ddd;
    border-radius: 8px;
    width: 450px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    font-family: "Wix Madefor Display", sans-serif;
}

.title-container {
    display: flex;
    align-items: center;
}

.form-title {
    font-size: 24px;
    font-weight: bold;
    color:  #21255b;
    font-family: "Wix Madefor Display", sans-serif;
}

.profile-icon {
    width: 90px;
    height: 90px;
    margin-left: 200px;
    border-radius: 50%;
    border: 2px solid #ccc;
}

label {
    align-self: flex-start;
    margin-bottom: 10px;
    font-weight: bold;
    color: #333;
    font-family: "Wix Madefor Display", sans-serif;
    transition: border 0.3s ease;
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

.row {
    display: flex;
    width: 100%;
    gap: 40px;
    margin-left: -20px;
}

.column {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
}

.column label {
    margin-left: 10px;
    display: inline-block;
    margin-bottom: 5px;
    font-weight: bold;
    color: #333;
    font-family: "Wix Madefor Display", sans-serif;
}

.button-group {
    display: flex;
    width: 100%;
    justify-content: space-between;
}

.save-btn,
.cancel-btn {
    padding: 12px 24px;
    border: none;
    border-radius: 5px;
    font-size: 16px;
    font-weight: bold;
    cursor: pointer;
    transition: background-color 0.3s ease;
}

.save-btn {
    background-color: #21255b;
    color: white;
}

.cancel-btn {
    background-color: #e53935;
    color: white;
}

.save-btn:hover {
    background-color: #343870;
}

.cancel-btn:hover {
    background-color: #d32f2f;
}

.username-container,
.email-container,
.password-container {
    display: flex;
    align-items: center;
    position: relative;
    width: 108%;
}

.user-icon {
    top: 50%;
    transform: translateY(-50%);
    width: 18px;
    height: 18px;
    fill: #555;
    pointer-events: none;
}

.email-icon {
    position: absolute;
    left: 13px;
    color: #555;
    font-size: 18px;
    margin-top: -15px;
    pointer-events: none;
}

.phone-icon {
    transform: translateX(-470%);
    width: 18px;
    height: 18px;
    fill: #555;
    margin-top: 20px;
    pointer-events: none;
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

.email-icon {}
</style>

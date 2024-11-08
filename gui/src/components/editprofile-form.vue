<template>
<div class="edit-form">
  <h2 class="form-title">Edit Profile</h2>
  
  <label for="username">Username</label>
  <input v-model="username" type="text" id="username" placeholder="Enter a username..." />
  
  <div class="row">
    <div class="column">
      <label for="name">Name(s)</label>
      <input v-model="name" type="text" id="name" placeholder="Enter your name or names..." />
    </div>
    <div class="column">
      <label for="lastName">Last Name(s)</label>
      <input v-model="lastName" type="text" id="lastName" placeholder="Enter your last name..." />
    </div>
  </div>
  
  <label for="email">E-mail</label>
  <input v-model="email" type="email" id="email" placeholder="Enter your email..." />
  <label for="curp">CURP</label>
  <input v-model="curp" type="text" id="curp" placeholder="Enter your CURP..." />
  <label for="rfc">RFC</label>
  <input v-model="rfc" type="text" id="rfc" placeholder="Enter your RFC..." />
  
  <div class="row">
    <div class="column">
      <label for="phone">Phone Number</label>
      <input v-model="phone" type="tel" id="phone" placeholder="Enter your phone number..." />
    </div>
    <div class="column">
      <label for="birthDate">Date of Birth</label>
      <input v-model="birthDate" type="date" id="birthDate" />
    </div>
  </div>
  
  <label for="password">Password</label>
  <input v-model="password" type="password" id="password" placeholder="Insert a password..." />
  
  <div class="button-group">
    <button class="cancel-btn" @click="$emit('goToHome')" >Cancel</button>
    <button class="save-btn" @click="saveProfile" >Save Changes</button>
  </div>
</div>
</template>

<script>
export default {
  name: 'EditProfileForm',
  props: {
    initialData: {
      type: Object,
      default: () => ({})
    }
  },
  data() {
    return {
      formData: {
	username: this.initialData.username || '',
        name: this.initialData.name || '',
        lastName: this.initialData.lastName || '',
        email: this.initialData.email || '',
        curp: this.initialData.curp || '',
        rfc: this.initialData.rfc || '',
        phone: this.initialData.phone || '',
        birthDate: this.initialData.birthDate || '',
        password: this.initialData.password || ''
      }
    };
  },
  methods: {
    saveProfile() {
      const sanitizedData = Object.fromEntries(
        Object.entries(this.formData).map(([key, value]) => [key, value || null])
      );

      this.$emit('saveProfile', sanitizedData);
    },
    goToHome() {
      this.$emit('goToHome');
    }
  }
};
</script>

<style scoped>
/* Sign-up form styling */
.edit-form {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  width: 400px;
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

/* Row for two-column layout */
.row {
  display: flex;
  width: 100%;
  gap: 10px;
}

/* Half-width for columns */
.column {
  flex: 1;
}

.button-group {
  display: flex;
  width: 100%;
  justify-content: space-between;
}

.save-btn {
    padding: 10px 20px;
    border: none;
    border-radius: 4px;
    font-size: 14px;
    cursor: pointer;
    background-color: #21255B;
    color: white;
    margin-bottom: 15px;
    font-family: "Wix Madefor Display", sans-serif;
}

.cancel-btn {
    padding: 10px 20px;
    border: none;
    border-radius: 4px;
    font-size: 14px;
    cursor: pointer;
    background-color: #333;
    color: white;
    font-family: "Wix Madefor Display", sans-serif;
}

.save-btn:hover .cancel-btn:hover{
  opacity: 0.9;
}
</style>

<template>
  <div class="form-container">
    <div class="edit-form">
      <h2 class="form-title">Edit Profile</h2>

      <label for="username">Username</label>
      <input
        v-model="formData.username"
        type="text"
        id="username"
        placeholder="Enter a username..."
      />

      <div class="row">
        <div class="column">
          <label for="name">Name(s)</label>
          <input
            v-model="formData.name"
            type="text"
            id="name"
            placeholder="Enter your name or names..."
          />
        </div>
        <div class="column">
          <label for="lastName">Last Name(s)</label>
          <input
            v-model="formData.lastName"
            type="text"
            id="lastName"
            placeholder="Enter your last name..."
          />
        </div>
      </div>

      <label for="email">E-mail</label>
      <input
        v-model="formData.email"
        type="email"
        id="email"
        placeholder="Enter your email..."
      />
      <label for="curp">CURP</label>
      <input
        v-model="formData.curp"
        type="text"
        id="curp"
        placeholder="Enter your CURP..."
      />
      <label for="rfc">RFC</label>
      <input
        v-model="formData.rfc"
        type="text"
        id="rfc"
        placeholder="Enter your RFC..."
      />

      <div class="row">
        <div class="column">
          <label for="phone">Phone Number</label>
          <input
            v-model="formData.phone"
            type="tel"
            id="phone"
            placeholder="Enter your phone number..."
          />
        </div>
        <div class="column">
          <label for="birthDate">Date of Birth</label>
          <input v-model="formData.birthDate" type="date" id="birthDate" />
        </div>
      </div>

      <label for="password">Password</label>
      <input
        v-model="formData.password"
        type="password"
        id="password"
        placeholder="Insert a password..."
      />

      <div class="button-group">
        <button class="cancel-btn" @click="$emit('goToHome')">Cancel</button>
        <button class="save-btn" @click="saveProfile">Save Changes</button>
      </div>
    </div>
  </div>
</template>

<script>
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
      },
    };
  },
  methods: {
    saveProfile() {
      const sanitizedData = Object.fromEntries(
        Object.entries(this.formData).map(([key, value]) => [
          key,
          value || null,
        ]),
      );
      console.log("Data to send:", sanitizedData);
      this.$emit("saveProfile", sanitizedData);
    },
    goToHome() {
      this.$emit("goToHome");
    },
  },
};
</script>

<style scoped>
.form-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f9f9f9;
}

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

label {
  align-self: flex-start;
  margin-bottom: 5px;
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
  background-color: #1b1e50;
}

.cancel-btn:hover {
  background-color: #d32f2f;
}

.save-btn:hover .cancel-btn:hover {
  opacity: 0.9;
}
</style>

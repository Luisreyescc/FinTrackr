<template>
  <div class="signup-page">
    <img src="@/assets/profile_black.svg" alt="Profile Icon" class="profile-icon" />
    <sign-up-form @signUp="signUp" @goToLogin="goToLogin" />
  </div>
</template>

<script>
import SignUpForm from '../formats/signup-form.vue';
import apiClient from "@/apiClient.js";

export default {
  name: "SignUp",
  components: {
    SignUpForm,
  },
  methods: {
    async signUp({ username, email, password, password2 }) {
      if (username && email && password && password2) {
        try {
          const response = await apiClient.post("register/", {
            user_name: username,
            email: email,
            password: password,
            password2: password2,
          });

          if (response.status === 201) {
            alert("User registered successfully! Redirecting to login...");
            this.$router.push("/login");
          } else {
            alert(response.data.error || "Registration failed");
          }
        } catch (error) {
          console.error("Registration error:", error);
          if (error.response && error.response.data) {
            const errors = [];
            for (const key in error.response.data) {
              errors.push(`${key}: ${error.response.data[key]}`);
            }
            alert(errors.join("\n"));
          } else {
            alert(
              "There was an issue with the registration. Please try again.",
            );
          }
        }
      } else {
        alert("Please fill in all required fields.");
      }
    },
    goToLogin() {
      this.$router.push("/login");
    },
  },
};
</script>

<style scoped>
.signup-page {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding-top: 190px;
    font-family: "Wix Madefor Display", sans-serif;
}

.profile-icon {
    width: 100px;
    height: 100px;
    margin-bottom: 20px;
    border-radius: 50%;
    border: 2px solid #ccc;
}
</style>

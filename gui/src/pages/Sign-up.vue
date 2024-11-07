<template>
  <div class="signup-page">
    <!-- Profile Icon -->
    <img
      src="@/assets/profile_black.svg"
      alt="Profile Icon"
      class="profile-icon"
    />
    <sign-up-form @signUp="signUp" @goToLogin="goToLogin" />
  </div>
</template>

<script>
import SignUpForm from "../components/signup-form.vue";
import axios from "axios";

export default {
  name: "SignUp",
  components: {
    SignUpForm,
  },
  methods: {
    async signUp({
      username,
      email,
      password,
      name,
      last_name,
      phone,
      curp,
      rfc,
      birth_date,
    }) {
      if (username && email && password) {
        try {
          // Formatea birth_date si no está en el formato esperado
          const formattedBirthDate = birth_date
            ? new Date(birth_date).toISOString().split("T")[0]
            : null;

          const response = await axios.post(
            "http://localhost:8000/api/auth/register/",
            {
              user_name: username,
              email: email,
              password_hash: password,
              name: name,
              last_name: last_name,
              phone: phone,
              curp: curp,
              rfc: rfc,
              birth_date: formattedBirthDate, // Usa la fecha formateada
            },
            {
              headers: {
                "Content-Type": "application/json",
              },
            },
          );

          if (response.status === 500) {
            alert("Signup failed");
          } else {
            alert("User registered! Redirecting to login...");
            this.$router.push("/");
          }
        } catch (error) {
          // Muestra detalles del error
          console.error(
            "Signup failed:",
            error.response ? error.response.data : error,
          );
          alert("There was an issue with your signup. Please try again.");
        }
      } else {
        alert("Please fill all required fields.");
      }
    },
    goToLogin() {
      this.$router.push("/");
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
  height: 100vh;
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

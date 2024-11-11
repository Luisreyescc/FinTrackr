<template>
  <div class="edit-profile-page">
    <EditProfileForm :initialData="userData" @saveProfile="editProfile" @goToHome="goToHome" />
  </div>
</template>

<script>
import EditProfileForm from '@/formats/editprofile-form.vue';
import axios from 'axios';

export default {
  name: "EditProfile",
  components: {
    EditProfileForm,
  },
  data() {
    return {
      userData: {
        user_name: "",
        name: "",
        last_name: "",
        email: "",
        phone: "",
        curp: "",
        rfc: "",
        birth_date: "",
        password: "",
      },
    };
  },
  methods: {
    async editProfile(profileData) {
      const dataToSend = {
        user_name: profileData.username,
        name: profileData.name,
        last_name: profileData.lastName,
        email: profileData.email,
        phone: profileData.phone,
        curp: profileData.curp,
        rfc: profileData.rfc,
        birth_date: profileData.birthDate,
        password: profileData.password,
      };
      try {
        const token = localStorage.getItem("token");
        const response = await axios.put(
          "http://localhost:8000/api/profile-details/",
          dataToSend,
          {
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${token}`,
            },
          },
        );
        if (response.status === 200) {
          alert("User data updated successfully!");
        } else {
          alert("Failed to save data");
        }
      } catch (error) {
        console.error("Update failed:", error);
        alert(
          error.response?.data?.message ||
            "An error occurred while updating the profile.",
        );
      }
    },
    goToHome() {
      this.$router.push("/");
    },
  },
};
</script>

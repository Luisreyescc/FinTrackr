<template>
  <div class="edit-profile-page">
    <EditProfileForm
      :initialData="userData"
      @saveProfile="editProfile"
      @goToHome="goToHome"
    />
  </div>
</template>

<script>
import EditProfileForm from "@/components/editprofile-form.vue";
import axios from "axios";

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
      const dataToSend = {};
      if (profileData.user_name) dataToSend.user_name = profileData.user_name;
      if (profileData.name) dataToSend.name = profileData.name;
      if (profileData.last_name) dataToSend.last_name = profileData.last_name;
      if (profileData.email) dataToSend.email = profileData.email;
      if (profileData.curp) dataToSend.curp = profileData.curp;
      if (profileData.rfc) dataToSend.rfc = profileData.rfc;
      if (profileData.phone) dataToSend.phone = profileData.phone;
      if (profileData.birth_date)
        dataToSend.birth_date = profileData.birth_date;

      if (profileData.password) {
        dataToSend.password_hash = profileData.password;
      }

      console.log("Data to send:", dataToSend);

      try {
        const response = await axios.put(
          "http://localhost:8000/api/profile-details/",
          dataToSend,
          {
            headers: {
              "Content-Type": "application/json",
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
        console.log("Error details:", error.response?.data);
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

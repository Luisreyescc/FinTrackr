<template>
  <div class="edit-profile-page">
    <div class="message-container">
      <MessageAlerts
        v-for="(msg, index) in messages"
        :key="msg.id"
        :text="msg.text"
        :type="msg.type"
        @close="removeMessage(index)"/>
    </div>
    <EditProfileForm
      :initialData="userData"
      @saveProfile="editProfile"
      @goToHome="goToHome"/>
  </div>
</template>

<script>
import EditProfileForm from "@/formats/editprofile-format.vue";
import MessageAlerts from "@/components/messages.vue";
import axios from "axios";

export default {
  name: "EditProfile",
  components: {
    EditProfileForm,
    MessageAlerts,
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
      messages: [],
    };
  },
  methods: {
    addMessage(text, type = "neutral") {
      const id = Date.now();
      this.messages.push({ id, text, type });
    },
    removeMessage(index) {
      this.messages.splice(index, 1);
    },
    async fetchUserData() {
      try {
        const token = localStorage.getItem("token");
        const response = await axios.get(
          "http://localhost:8000/api/profile-details/",
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          },
        );
        if (response.status === 200) {
          this.userData = {
            user_name: response.data.user_name || "",
            name: response.data.name || "",
            last_name: response.data.last_name || "",
            email: response.data.email || "",
            phone: response.data.phone || "",
            curp: response.data.curp || "",
            rfc: response.data.rfc || "",
            birth_date: response.data.birth_date || "",
            password: "", // We leave password field empty for security reasons
          };
        }
      } catch (error) {
        console.error("Error fetching user data:", error);
        this.addMessage("Failed to fetch your data", "error");
      }
    },
    async editProfile(profileData) {
      const dataToSend = {
        user_name: profileData.user_name,
        name: profileData.name,
        last_name: profileData.last_name,
        email: profileData.email,
        phone: profileData.phone,
        curp: profileData.curp,
        rfc: profileData.rfc,
        birth_date: profileData.birth_date,
        password: profileData.password,
        new_password: profileData.new_password,
        confirm_password: profileData.confirm_password,
      };
      try {
        const token = localStorage.getItem("token");
        if (!token) {
          console.error("No token found");
          return;
        }
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
        console.log("API response:", response);
        if (response.status === 200) {
          this.addMessage("User data updated succesfully.", "success");
        } else {
          this.addMessage("Failed to save your data.", "error");
        }
      } catch (error) {
        console.error("Update failed:", error);
        this.addMessage("An error occure while saving your data.", "error");
      }
    },
    goToHome() {
      this.$router.push("/");
    },
  },
  mounted() {
    console.log("Mounted hook is working");
    this.fetchUserData(); // Fetch user data when component is mounted
  },
};
</script>

<style scoped>
.edit-profile-page {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    background: #25262B;
    font-family: "Wix Madefor Display", sans-serif;
}
</style>

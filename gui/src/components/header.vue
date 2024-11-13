<template>
  <header class="header">
    <div class="header-content">
      <img src="@/assets/title.svg" alt="FinTrackr Logo" class="logo" />

      <!-- Display menu if user is logged in -->
      <div class="nav-profile-wrapper">
        <nav v-if="isLoggedIn" class="nav-menu">
          <router-link to="/home" class="nav-item">Home<span></span></router-link>
          <router-link to="/status" class="nav-item">Status<span></span></router-link>
          <router-link to="/history" class="nav-item">History<span></span></router-link>
          <router-link to="/leaderboard" class="nav-item">Leaderboard<span></span></router-link>
        </nav>

        <!-- Welcome Message and Profile Icon with Dropdown -->
        <div v-if="isLoggedIn" class="profile-menu">
          <span class="welcome-message"> {{ userName }}</span>
          <img
            src="@/assets/profile_white.svg"
            alt="Profile"
            class="profile-icon"
            @click="toggleDropdown"
          />
          <div v-if="dropdownOpen" class="dropdown">
            <button @click="editProfile">Edit Profile</button>
            <button @click="logout">Sign-out</button>
          </div>
        </div>
      </div>
    </div>
  </header>
</template>

<script>
import axios from "axios";

export default {
  name: "AppHeader",
  props: {
    isLoggedIn: Boolean,
  },
  data() {
    return {
      dropdownOpen: false,
      userName: "", // Almacena el nombre del usuario
    };
  },
  created() {
    this.fetchUserName();
  },
  methods: {
    toggleDropdown() {
      this.dropdownOpen = !this.dropdownOpen;
    },
    async fetchUserName() {
      try {
        const token = localStorage.getItem("token");
        if (token) {
          const response = await axios.get("http://localhost:8000/api/profile/", {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          });
          this.userName = response.data.user_name; // Asigna el user_name desde la respuesta
        }
      } catch (error) {
        console.error("Error fetching user name:", error);
      }
    },
    editProfile() {
      this.$router.push("/edit-profile");
    },
    logout() {
      sessionStorage.removeItem("isLoggedIn");
      localStorage.removeItem("token");
      this.$router.push("/");
    },
  },
};
</script>

<style scoped>
.header {
  background-color: #21255b;
  padding: 13px;
  color: #ffffff;
  width: 100%;
  position: fixed;
  top: 0;
  left: 0;
  z-index: 1000;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-right: 25px;
}

.logo {
  height: 40px;
  width: auto;
}

.nav-profile-wrapper {
  display: flex;
  align-items: center;
  gap: 15px;
}

.nav-menu {
  display: flex;
  gap: 0;
  margin-left: 0;
  padding: 0;
}

.nav-item {
  color: #ffffff;
  text-decoration: none;
  font-size: 20px;
  padding: 12px 20px;
  position: relative;
  overflow: hidden;
  transition: color 0.5s;
}

.nav-item:hover {
  color: #21255B;
}

.profile-menu {
  position: relative;
  display: flex;
  align-items: center;
}

.welcome-message {
  margin-right: 10px;
  color: #ffffff;
  font-size: 18px;
}

.profile-icon {
  width: 45px;
  cursor: pointer;
}

.dropdown {
  position: absolute;
  top: 60px;
  right: 0;
  background: #ffffff;
  color: #333;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
  width: 150px;
  padding: 8px 0;
  display: flex;
  flex-direction: column;
}

.dropdown button {
  width: 100%;
  padding: 10px 15px;
  background: transparent;
  border: none;
  color: #333;
  text-align: left;
  font-size: 16px;
  cursor: pointer;
  transition: background 0.2s ease, color 0.2s ease;
}

.dropdown button:hover {
  background-color: #e4ecfa;
  color: #5860d0;
}

.dropdown button:focus {
  outline: none;
}
</style>

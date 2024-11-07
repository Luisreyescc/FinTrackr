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

      <!-- Profile Icon with Dropdown -->
      <div v-if="isLoggedIn" class="profile-menu">
        <img src="@/assets/profile_white.svg" alt="Profile" class="profile-icon" @click="toggleDropdown" />
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
export default {
  name: 'AppHeader',
  props: {
    isLoggedIn: Boolean //
  },
  data() {
    return {
      dropdownOpen: false
    };
  },
  methods: {
    toggleDropdown() {
      this.dropdownOpen = !this.dropdownOpen;
    },
    editProfile() {
      alert("Edit Profile clicked");
    },
    logout() {
      this.$emit('logout');
    }
  }
};
</script>

<style scoped>
.header {
  background-color: #21255B;
  padding: 13px;
  color: #FFFFFF;
  width: 100%;
  position: fixed; /* Make the banner stick at the top of the page */
  top: 0;
  left: 0;
  z-index: 1000; /* Ensure it stays on top of other elements */
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
  gap: 15px; /* Space between nav menu and profile icon */
}

.nav-menu {
    display: flex;
    gap: 0;
    margin-left: 0;
    padding: 0;
}

.nav-item {
  color: #FFFFFF;
  text-decoration: none;
  font-size: 20px;
  padding: 12px 20px;
  position: relative;
  overflow: hidden;
  transition: color 0.5s;
}

.nav-item:hover {
  color: #5860D0;
}

.nav-item::before,
.nav-item::after,
.nav-item span::before,
.nav-item span::after {
  content: "";
  position: absolute;
  height: 100%;
  width: 25%;
  top: 0;
  left: 0;
  background: #FFFFFF;
  transform: translateY(-110%);
  transition: transform 0.5s;
  z-index: -1;
}

.nav-item:hover::before,
.nav-item:hover::after,
.nav-item:hover span::before,
.nav-item:hover span::after {
  transform: translateY(0);
}

.nav-item::after {
  left: 25%;
  transition-delay: 0.1s;
}

.nav-item span::before {
  left: 50%;
  transition-delay: 0.2s;
}

.nav-item span::after {
  left: 75%;
  transition-delay: 0.3s;
}

.profile-menu {
  position: relative;
}

.profile-icon {
  width: 45px;
  cursor: pointer;
}

.dropdown {
  position: absolute;
  top: 60px;
  right: 0;
  background: #FFFFFF;
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
  background-color: #E4ECFA;
  color: #5860D0;
}

.dropdown button:focus {
  outline: none;
}
</style>

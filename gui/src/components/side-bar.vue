<template>
<div>
  <div v-if="isVisible" class="overlay" @click="$emit('closeSidebar')"></div>
<div class="side-bar" :class="{ 'side-bar--visible': isVisible }">
  
  <div class="sidebar-logo">
    <img src="@/assets/title.svg" alt="Logo" class="logo">
  </div>
  
  <button @click="$emit('closeSidebar')" class="close-button">
    <span class="gg-close"></span>
  </button>
  
  <!-- Sidebar menu options -->
  <div class="menu-options">
    <button @click="selectOption('Incomes')" class="menu-option">
      <span class="gg-trending">
      </span> Incomes</button>
    <button @click="selectOption('Expenses')" class="menu-option">
      <span class="gg-trending-down">
      </span>Expenses</button>
    <button @click="selectOption('Debts')" class="menu-option">
      <img src="@/assets/card.svg" alt="Debts Icon" class="icon"> Debts</button>
  </div>
  
  <div class="bottom-options">
    <button @click="editProfile" class="edit-profile-btn">
      <span class="gg-user"></span> Edit Profile</button>
    <button @click="logout" class="logout-btn">Log-out</button>
  </div>
</div>
</div>
</template>

<script>
import '@/css/close.css';
import '@/css/down.css';
import '@/css/up.css';

export default {
  name: "SideBar",
  props: {
    isVisible: {
      type: Boolean,
      default: false
    }
  },
  methods: {
    selectOption(option) {
      this.$emit('selectContent', option);
    },
    editProfile() {
      this.$router.push('/edit-profile');
    },
    logout() {
      console.log('User logged out');
    }
  }
};
</script>

<style scoped>
.overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: rgba(0, 0, 0, 0.5);
    backdrop-filter: blur(3px);
    z-index: 1000;
}

.side-bar {
    width: 350px;
    height: 100%;
    background-color: #212352;
    color: white;
    position: fixed;
    top: 0;
    left: 0;
    transform: translateX(-100%);
    transition: transform 0.4s cubic-bezier(0.25, 1, 0.5, 1);
    z-index: 1000;
    padding-top: 60px;
}

.side-bar--visible {
    transform: translateX(0);
}

.sidebar-logo {
    text-align: left;
    padding-left: 20px;
    padding-bottom: 20px;
}

.sidebar-logo .logo {
    width: 150px;
    height: auto;
}

.close-button .gg-close {
    background: none;
    border: none;
    color: white;
    position: absolute;
    top: 15px;
    right: 15px;
    cursor: pointer;
}

.menu-options {
    padding: 0;
}

.menu-option .gg-trending {
    color: white;
    margin-top: 8px;
    margin-right: 22px;
}

.menu-option .gg-trending-down {
    color: white;
    margin-bottom: 8px;
    margin-right: 22px;
}

.menu-option img.icon {
    width: 20px;
    height: 20px;
    margin-right: 12px;
}

.bottom-options {
    margin-top: 450px;
    padding-bottom: 20px;
    display: flex;
    flex-direction: column;
    align-items: center;
}

.menu-option {
    margin: 10px 8px;
    background-color: #212352;
    color: #ffffff;
    padding: 15px 20px;
    border: none;
    border-radius: 8px;
    width: 95%;
    text-align: left;
    font-size: 20px;
    cursor: pointer;
    display: flex;
    padding-left: 40px;
    align-items: center;
    line-height: 40px;
    font-weight: bold;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    border-bottom: 1px solid black;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    transition: 0.4s;
}

.menu-option:hover {
    padding-left: 50px;
    background-color: #2F316B;
    transform: scale(1.05);
}

.menu option {
    margin-right: 16px;
}

.menu-option {
    margin: 10px 8px;
    background-color: #212352;
    color: #ffffff;
    padding: 15px 20px;
    border: none;
    border-radius: 8px;
    width: 95%;
    text-align: left;
    font-size: 20px;
    cursor: pointer;
    display: flex;
    padding-left: 40px;
    align-items: center;
    line-height: 40px;
    font-weight: bold;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    border-bottom: 1px solid black;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    transition: 0.4s;
}

.menu-option:hover {
    padding-left: 50px;
    background-color: #2F316B;
    transform: scale(1.05);
}

.edit-profile-btn {
    padding: 14px 16px;
    border: 1px solid #ffffff;
    border-radius: 10px;
    font-size: 15px;
    cursor: pointer;
    background-color: #ffffff;
    color: #333;
    font-weight: bold;
    margin-bottom: 10px;
    width: 60%;
    text-align: center;
    transition: background-color 0.3s ease, color 0.3s ease, border 0.3s ease;
    box-shadow: 0px 2px 6px rgba(0, 0, 0, 0.1);
}

.edit-profile-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 10px 25px;
    border: 2px solid #ffffff;
    border-radius: 20px;
    font-size: 14px;
    cursor: pointer;
    background-color: #ffffff;
    color: #333333;
    font-weight: bold;
    margin-bottom: 10px;
    width: 60%;
    text-align: center;
    transition: background-color 0.3s ease, color 0.3s ease;
}

.edit-profile-btn:hover {
    background-color: #333333;
    color: #ffffff;
}

.edit-profile-btn .gg-user {
    margin-right: 10px;
}

.logout-btn {
    padding: 10px 25px;
    border: 2px solid #ffffff;
    border-radius: 20px;
    font-size: 14px;
    cursor: pointer;
    background-color: transparent;
    color: #ffffff;
    font-weight: bold;
    width: 60%;
    text-align: center;
    transition: background-color 0.3s ease, color 0.3s ease;
}

.logout-btn:hover {
    background-color: #333333;
    color: #ffffff;
}

.menu option {
    margin-right: 16px;
}
</style>

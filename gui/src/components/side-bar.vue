<template>
<div>
  <div v-if="isVisible" class="overlay" @click="$emit('closeSidebar')"></div>
  <div class="side-bar" :class="{ 'side-bar--visible': isVisible }">
    <button @click="$emit('closeSidebar')" class="close-button">
      <font-awesome-icon :icon="['fas', 'xmark']" class="close-button"/>
    </button>
    
    <div class="sidebar-logo">
      <font-awesome-icon :icon="['fab', 'docker']" class="logo-icon"/>
      <img src="@/assets/title.svg" alt="Logo" class="logo">
    </div>  
    
    <div class="divider_top"></div>
    
    <div v-if="currentPage === 'Home'" class="menu-options">
      <button @click="selectOption('Incomes')" class="menu-option">
	<font-awesome-icon :icon="['fas', 'chart-line']" class="icon"/> Incomes</button>
      <button @click="selectOption('Expenses')" class="menu-option">
	<font-awesome-icon :icon="['fas', 'money-bill-transfer']" class="icon"/> Expenses</button>
      <button @click="selectOption('Debts')" class="menu-option">
	<font-awesome-icon :icon="['fas', 'credit-card']" class="icon"/> Debts</button>
    </div>

    <div v-if="currentPage === 'Status'" class="menu-options">
      <button @click="selectOption('Account')" class="menu-option">
	<font-awesome-icon :icon="['fas', 'chart-area']" class="icon a"/>Account Status</button>
      <button @click="selectOption('Categories')" class="menu-option">
	<font-awesome-icon :icon="['fas', 'chart-pie']" class="icon a"/>Categories Pie</button>
    </div>
    
    <div class="divider_bottom"></div>
    
    <div class="bottom-options">
      <button @click="editProfile" class="bottom-option">
	<font-awesome-icon :icon="['fas', 'pen-to-square']" class="icon"/> Edit Profile</button>
      <button @click="logout" class="bottom-option">
        <font-awesome-icon :icon="['fas', 'right-from-bracket']" class="icon"/> Log-out</button>
    </div>
  </div>
</div>
</template>

<script>
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';

export default {
  name: "SideBar",
  components: {
    FontAwesomeIcon,
  },
  props: {
    isVisible: {
      type: Boolean,
      default: false
    },
    currentPage: {
      type: String,
      required: true
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
      sessionStorage.removeItem("isLoggedIn");
      localStorage.removeItem("token");
      this.$router.push("/");
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
    background: rgba(59, 59, 90, 0.5);
    backdrop-filter: blur(3px);
    z-index: 1000;
}

.side-bar {
    width: 350px;
    height: 100%;
    background-color: #25253C;
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

.close-button  {
    background: none;
    border: none;
    color: white;
    position: absolute;
    top: 10px;
    right: 13px;
    font-size: 24px;
    cursor: pointer;
}

.sidebar-logo {
    display: flex;
    align-items: center;
    padding-top: 30px;
    padding-left: 20px;
    padding-bottom: 0;
}

.logo-icon {
    margin-right: 10px;
    font-size: 32px;
}

.logo {
    width: 150px;
    height: auto;
}

.divider_top {
    height: 2px;
    background: white;
    margin: 40px 20px;
    opacity: 0.8;
}

.menu-options, .bottom-options {
    display: flex;
    flex-direction: column;
    margin-top: 20px;
}

.menu-option, .bottom-option {
    display: flex;
    align-items: center;
    text-align: left;
    padding: 15px 35px;
    margin: 10px;
    width: 85%;
    border-radius: 8px;
    line-height: 40px;
    background: none;
    border: none;
    color: white;
    font-size: 24px;
    font-weight: bold;
    cursor: pointer;
    transition: all 0.4s ease;
    font-family: "Wix Madefor Display", sans-serif;
}

.icon {
    margin-right: 30px;
    font-size: 24px;
}

.icon.a {
    margin-right: 15px;
}
.menu-option:hover, .bottom-option:hover {
    background-color: #3B3B5A;
    transform: translateX(10px);
}

.divider_bottom {
    height: 2px;
    background: white;
    margin: 250px 20px;
    opacity: 0.8;
}

.bottom-options {
    margin-top: -220px;
}

.bottom-option {
    font-size: 22px;
}
</style>

<template>
<div class="page-container scrollbar">
  <SideBar
    :isVisible="isSidebarVisible"
    :currentPage="'UsersManagment'"
    @closeSidebar="toggleSidebar"
    @selectContent="updateContent"/>
  <div class="sidebar">
    <button @click="toggleSidebar" class="menu-button" :class="{ 'hidden': isSidebarVisible }">
      <font-awesome-icon :icon="['fas', 'bars']" font-size="38"/>
    </button>
  </div>
  
  <div class="content-wrapper">
    <div v-if="selectedContent === 'UsersManagment'" class="main-content">
      <div class="events-container">
        <div class="header">
          <h2 class="section-title">Users Management</h2>
          <UsersHeader @resetClicked="handleResetClick" @search="handleSearch"/>
        </div>
        <div class="activity-content">
          <h3 class="activity-title">Users</h3>
          <div class="list-container scrollbar">
            <span v-if="loadingUsers">Loading users...</span>
            <UserRow v-for="user in filteredUsers" :key="user.user_id" :user="user" @userDeleted="fetchUsers"/>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
</template>

<script>
import axios from 'axios';
import UsersHeader from '@/components/users-header.vue';
import UserRow from '@/components/user-row.vue';
import SideBar from '@/components/side-bar.vue';
import '@/css/scrollbar.css';

export default {
  name: "UsersManagment",
  components: {
    UsersHeader,
    UserRow,
    SideBar
  },
  data() {
    return {
      isSidebarVisible: false,
      selectedContent: 'UsersManagment',
      users: [],
      filteredUsers: [],
      searchQuery: '',
      loadingUsers: false
    };
  },
  methods: {
    toggleSidebar() {
      this.isSidebarVisible = !this.isSidebarVisible;
    },
    updateContent(content) {
      this.selectedContent = content;
      this.isSidebarVisible = false;
    },
    async fetchUsers() {
      this.filteredUsers = this.users;
      try {
        this.loadingUsers = true;
        const response = await axios.get("http://localhost:8000/api/admin/financial-summary/", {
          headers: { Authorization: `Bearer ${localStorage.getItem("token")}` }
        });
        this.users = response.data;
        this.filteredUsers = this.users;
      } catch (error) {
        console.error("Error fetching users:", error);
      } finally {
        this.loadingUsers = false;
      }
    },
    searchUsers(query) {
      this.searchQuery = query;
      this.filteredUsers = this.users.filter(user => 
        user.user_name.toLowerCase().includes(query.toLowerCase()) ||
        user.email.toLowerCase().includes(query.toLowerCase())
      );
    },
    resetFilters() {
      this.searchQuery = '';
      this.filteredUsers = this.users;
    },
    handleResetClick() {
      this.resetFilters();
    },
    handleSearch(query) {
      this.searchQuery = query;
      this.searchUsers(query);
    }
  },
  created() {
    this.fetchUsers();
  }
};
</script>

<style scoped>
.page-container {
    display: flex;
    position: relative;
    justify-content: space-between;
    padding-top: 100px;
    min-height: 100vh;
    background: #25262B;
    font-family: "Wix Madefor Display", sans-serif;
}

.sidebar {
    width: 50px;
    display: flex;
    align-items: center;
    justify-content: center;
    position: fixed;
    z-index: 1000;
    padding-top: 20px;
    font-family: "Wix Madefor Display", sans-serif;
}

.menu-button {
    padding: 20px;
    margin-top: -25px;
    margin-left: 35px;
    background: none;
    border: none;
    cursor: pointer;
    color: white;
    transition: transform 0.2s ease-in-out;
}

.menu-button:hover {
    transform: scale(1.1);
}

.menu-button.hidden {
    display: none;
}

.content-wrapper {
    flex: 1;
    display: flex;
    justify-content: center;
    padding: 20px;
    margin-left: 70px;
    position: relative;
}

.main-content {
    display: flex;
    flex-direction: column;
    max-width: 1200px;
    width: 100%;
    background: #25262B;
}

.header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 10px 20px;
    background: #25262B;
    border: 2px solid white;
    border-radius: 20px;
    font-family: "Wix Madefor Display", sans-serif;
}

.header h3 {
    font-size: 32px; 
}

.section-title {
    font-size: 32px;
    font-weight: bold;
    color: white;
    font-family: "Wix Madefor Display", sans-serif;
}

.activity-content {
    display: flex;
    flex-direction: column;
    max-height: 100vh;
    overflow: hidden;
    padding: 20px;
    border: 2px solid white;
    margin-top: 10px;
    border-radius: 20px;
    background: #25262B;
    position: relative;
}

.activity-title {
    font-size: 28px;
    font-weight: bold;
    margin-bottom: 10px;
    text-align: left;
    color: white;
    font-family: "Wix Madefor Display", sans-serif;
}

.list-container {
    flex: 1;
    overflow-y: auto;
    padding-right: 10px;
    border-radius: 12px;
    max-height: calc(70vh - 30px);
}
</style>

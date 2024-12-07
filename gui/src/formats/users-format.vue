<template>
<div class="users-form">
  <div class="sidebar">
    <button @click="toggleSidebar" class="menu-button">
      <font-awesome-icon :icon="['fas', 'bars']" font-size="38"/>
    </button>
  </div>
  
  <div class="content-wrapper">
    <div v-if="selectedContent === 'UsersManagment'" class="main-content">
      <div class="events-container">
        <div class="header">
          <h2 class="section-title">Users Managment</h2>
          <UsersHeader @resetClicked="handleResetClick" @search="handleSearch"/>
        </div>
        <div class="users-content">
          <h3 class="users-title">Users</h3>
          <div class="users-section">
            <div class="list-container scrollbar">
              <span v-if="loadingUsers">Loading users...</span>
              <UserRow v-for="(user, index) in filteredUsers" :key="index" :user="user"/>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>

<div class="message-container">
  <MessageAlerts
    v-for="(msg, index) in messages" 
    :key="msg.id" 
    :text="msg.text" 
    :type="msg.type" 
    @close="removeMessage(index)"/>
</div>
</template>

<script>
import axios from 'axios';
import '@/css/scrollbar.css';
import MessageAlerts from '@/components/messages.vue';

import UsersHeader from '@/components/users-header.vue';
import UserRow from '@/components/user-row.vue';

export default {
  name: "UsersForm",
  components: {
    UsersHeader,
    UserRow,
    MessageAlerts
  },
  props: {
    selectedContent: {
      type: String,
      default: 'UsersManagment'
    },
  },
  data() {
    return {
      user: [],
      messages: [],
      searchQuery: "",
      loadingUsers: false
    };
  },
  computed: {
    sortedUsers() {
      let user = 'user';
      return user;
    },
    filteredUsers() {
      let user = 'user';
      return user;
    }
  },
  methods: {
    addMessage(text, type = "neutral") {
      const id = Date.now();
      this.messages.push({ id, text, type });
    },
    removeMessage(index) {
      this.messages.splice(index, 1);
    },
    toggleSidebar() {
      this.$emit('toggleSidebar');
    },
    async fetchUsers() {
      try {
        const token = localStorage.getItem("token");
        if (!token)
          return console.error("No token found");

	this.loadingUsers = true;
        const response = await axios.get('http://localhost:8000/api/users/', {
          headers: { Authorization: `Bearer ${token}` },
        });
        const users = response.data.map((user) => ({
          ...user,
          type: 'User' // Add type field
        }));
        this.user.push(...users);
      } catch (error) {
        console.error('Error fetching incomes:', error);
        this.addMessage("There was an error fetching the users.", "error");
      } finally {
	this.loadingUsers = false;
      }
    },
    handleResetClick() {
      this.searchQuery = "";
    },
    handleSearch(query) {
      this.searchQuery = query;
    },
  },
  mounted() {
    if (this.selectedContent === "UsersManagment")
      this.fetchUsers();
  },
  watch: {
    selectedContent(newValue) {
      if (newValue === "UsersManagment")
        this.fetchUsers();
    }
  },
};
</script>

<style scoped>
.users-form {
    display: flex;
    width: 100%;
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

.users-content {
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

.users-title {
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

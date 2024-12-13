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
import moment from 'moment';
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
      searchQuery: '',
      loadingUsers: false
    };
  },
  computed: {
    filteredUsers() {
      let users = this.users;

      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase();
        const [filterType, filterValue] = query.includes(':') ? query.split(':').map(s => s.trim()) : [query, query];

        if (filterValue) {
          if (filterType === 'network ==') {
            users = users.filter(user => user.network.toString().startsWith(filterValue));
          } else if (filterType === 'network >=') {
            const network = parseFloat(filterValue);
            users = users.filter(user => user.network >= network);
          } else if (filterType === 'network <=') {
            const network = parseFloat(filterValue);
            users = users.filter(user => user.network <= network);
          } else if (filterType === 'birthday') {
            const dateFormats = ["YYYY-MM-DD", "YYYY-MMM-DD", "YYYY-MM", "YYYY-MMM", "YYYY", "MM", "MMM"];
            users = users.filter(user => {
              return dateFormats.some(format => {
                const userBirthDate = moment(user.birth_date, "YYYY-MM-DD");
                const filterDate = moment(filterValue, format);
                if (filterValue.length === 2 || filterValue.length === 3) {
                  return userBirthDate.isSame(filterDate, 'month');
                } else if (filterValue.length === 4) {
                  return userBirthDate.isSame(filterDate, 'year');
                } else if (filterValue.length === 7 || filterValue.length === 8) {
                  return userBirthDate.isSame(filterDate, 'month');
                } else {
                  return userBirthDate.isSame(filterDate, 'day');
                }
              });
            });
          } else if (filterType === 'username') {
            users = users.filter(user => user.user_name.toLowerCase().includes(filterValue.toLowerCase()));
          } else if (filterType === 'full name') {
            users = users.filter(user => {
              const fullName = `${user.name} ${user.last_name}`.toLowerCase();
              return fullName.includes(filterValue.toLowerCase());
            });
          } else {
            // Global search
            const network = parseFloat(filterValue);
            users = users.filter(user => {
              const fullName = `${user.name} ${user.last_name}`.toLowerCase();
              return (
                user.user_name.toLowerCase().includes(filterValue) ||
                user.email.toLowerCase().includes(filterValue) ||
                fullName.includes(filterValue) ||
                (!isNaN(network) && user.network === network)
              );
            });
          }
        }
      }

      return users;
    }
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
      try {
        this.loadingUsers = true;
        const response = await axios.get("http://localhost:8000/api/admin/financial-summary/", {
          headers: { Authorization: `Bearer ${localStorage.getItem("token")}` }
        });
        this.users = response.data;
      } catch (error) {
        console.error("Error fetching users:", error);
      } finally {
        this.loadingUsers = false;
      }
    },
    handleResetClick() {
      this.searchQuery = "";
    },
    handleSearch(query) {
      this.searchQuery = query;
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

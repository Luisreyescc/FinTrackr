<template>
  <div class="user-row">
    <div class="user-icon">
      <font-awesome-icon :icon="['fas', 'user-tie']" class="row-icon"/>
    </div>
    
    <div class="user-details">
      <h4>{{ user.user_name }}</h4>
      <p class="user-fullname">{{ formattedFullname }}</p>
      <p v-if="user.birth_date" class="user-bday">{{ formattedBDate }}</p>
      <p class="user-role">{{ userRole }}</p>
    </div>
    
    <div class="user-actions-section">
      <p class="user-network">{{ formattedNetwork }}</p>
      <div class="user-actions">
        <button class="full-button" @click="showFullData">
          <font-awesome-icon :icon="['fas', 'circle-info']" class="data-icon"/>
        </button>
        <button v-if="!isCurrentUser" class="delete-button" @click="showDeleteWarning">
          <font-awesome-icon :icon="['fas', 'trash-can']" class="trash-icon"/>
        </button>
      </div>
    </div>
    
    <div v-if="isFullData" class="overlay" @click="cancelFullData"></div>
    <div v-if="isFullData" class="data-popup">
      <h3 class="user-title">{{ user.user_name }}</h3>
      <div class="popup-content srollbar">
	<div class="labels-content">
          <label>Fullname:</label>
          <label>Email:</label>
          <label>CURP:</label>
          <label>RFC:</label>
          <label>Phone Number:</label>
          <label v-if="user.birth_date">Birth Date:</label>
          <label>Incomes:</label>
          <label>Expenses:</label>
          <label>Debts:</label>
          <label>Network:</label>
	</div>
	<div class="spans-content">
          <span>{{ formattedFullname || 'No data' }}</span>
          <span>{{ user.email || 'No data' }}</span>
          <span>{{ user.curp || 'No data' }}</span>
          <span>{{ user.rfc || 'No data' }}</span>
          <span>{{ user.phone || 'No data' }}</span>
          <span v-if="user.birth_date">{{ formattedBDate || 'No data' }}</span>
          <span>{{ formattedCurrency(user.incomes) || 'No data' }}</span>
          <span>{{ formattedCurrency(user.expenses) || 'No data' }}</span>
          <span>{{ formattedCurrency(user.debts) || 'No data' }}</span>
          <span>{{ formattedCurrency(user.network) || 'No data' }}</span>
	</div>
      </div>
      <button type="button" class="close-button" @click="cancelFullData">Close</button>
    </div>
    
    <div v-if="showDeletePopup" class="overlay" @click="cancelDelete"></div>
    <div v-if="showDeletePopup" class="delete-popup">
      <h3 class="warning-title">Warning</h3>
      <p>This action is permanent and cannot be undone.</p>
      <p>Are you sure you want to delete this user?</p>
      <div class="button-group">
        <button class="cancel-button" @click="cancelDelete">Cancel</button>
        <button class="confirm-delete-button" @click="confirmDelete">Delete</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { jwtDecode } from 'jwt-decode';

export default {
  name: 'UserRow',
  props: {
    user: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      isFullData: false,
      showDeletePopup: false,
      currentUserId: null
    };
  },
  computed: {
    isCurrentUser() {
      return this.user.user_id === this.currentUserId;
    },
    formattedFullname() {
      const fullname = `${this.user.name} ${this.user.last_name}`;
      return fullname.trim() ? fullname : 'No data';
    },
    formattedNetwork() {
      return this.formattedCurrency(this.user.network || 0);
    },
    formattedBDate() {
      if (!this.user.birth_date) return '';
      const date = new Date(this.user.birth_date);
      const day = String(date.getDate()).padStart(2, "0");
      const month = date.toLocaleString("en-US", { month: "short" }).toUpperCase();
      const year = date.getFullYear();
      return `${year}-${month}-${day}`;
    },
    userRole() {
      return this.user.is_staff ? 'Admin' : 'User';
    }
  },
  methods: {
    formattedCurrency(amount) {
      const formatter = new Intl.NumberFormat("en-US", {
        style: "currency",
        currency: "USD",
      });
      return formatter.format(amount || 0);
    },
    showFullData() {
      this.isFullData = true;
    },
    cancelFullData() {
      this.isFullData = false;
    },
    showDeleteWarning() {
      this.showDeletePopup = true;
    },
    cancelDelete() {
      this.showDeletePopup = false;
    },
    async confirmDelete() {
      try {
        await axios.delete(`http://localhost:8000/api/admin/delete-user/${this.user.user_id}/`, {
          headers: { Authorization: `Bearer ${localStorage.getItem("token")}` }
        });
        this.$emit('userDeleted', this.user.user_id);
        this.showDeletePopup = false;
      } catch (error) {
        console.error("Error deleting user:", error);
      }
    }
  },
  created() {
    const token = localStorage.getItem('token');
    if (token) {
      const decodedToken = jwtDecode(token);
      this.currentUserId = decodedToken.user_id;
    }
  }
};
</script>

<style scoped>
.user-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 15px;
    background: #25262B;
    border: 2px solid white;
    border-radius: 20px;
    margin-bottom: 10px;
    box-shadow: -2px 0 8px  rgba(255, 255, 255, 0.1);
}

.user-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 75px;
    height: 75px;
    border-radius: 50%;
    background: #25262B;
    border: 2px solid white;
    margin-right: 14px;
}

.row-icon {
    font-size: 40px;
    color: white;
}

.user-details {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    overflow: hidden;
}

.user-details h4, .user-fullname {
    margin: 0;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 420px;
    margin-left: 10px;
}

.user-details h4 {
    font-size: 22px;
    margin-bottom: 5px;
    color: #4DBEC8;
    font-weight: bold;
}

.user-details p {
    margin-top: 2px;
    margin-bottom: 2px;
}

.user-fullname {
    color: white;
    font-weight: bold;
    font-size: 20px;
}

.user-bday {
    color: #BF9F00;
    font-weight: bold;
    font-size: 18px;
    margin-left: 10px;
    white-space: nowrap;
}

.user-role {
    color: #6092DE;
    font-weight: bold;
    font-size: 18px;
    margin-left: 10px;
    white-space: nowrap;
}

.user-actions-section {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    margin-left: 25px;
}

.user-network {
    font-weight: bold;
    color: #7758BF;
    font-size: 20px;
    flex-shrink: 0;
}

.user-actions {
    display: flex;
    gap: 10px;
    margin-top: 2px;
}

.full-button, .delete-button {
    border-radius: 10px;
    cursor: pointer;
    width: 38px;
    height: 38px;
    display: flex;
    align-items: center;
    justify-content: center;
    border: none;
    transition: transform 0.2s, background-color 0.2s;
}

.full-button {
    background-color: white;
}

.full-button:hover {
    transform: scale(1.1);
    background-color: #F2F2F2;
}

.delete-button {
    background-color: #D55C5C;
    color: white;
}

.delete-button:hover {
    transform: scale(1.1);
    background-color: darkred;
}

.data-icon {
    font-size: 24px;
    color: #25262B;
}

.trash-icon {
    font-size: 20px;
    color: white;
}

.data-popup, .delete-popup {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background: #25262B;
    border-radius: 12px;
    padding: 20px;
    width: 600px;
    z-index: 1100;
    box-shadow: 0 4px 8px rgba(255, 255, 255, 0.2);
}

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

.popup-content {
    display: flex;
    justify-content: space-between;
    max-height: calc(80vh - 200px);
    padding: 10px;
    margin: 0;
    overflow-y: auto;
}

.user-title {
    font-size: 32px;
    font-weight: bold;
    text-align: center;
    margin-bottom: 20px;
    color: white;
    font-family: "Wix Madefor Display", sans-serif;
}

label {
    display: block;
    margin-bottom: 20px;
    font-weight: bold;
    font-size: 24px;
    color: white;
    text-align: left;
    font-family: "Wix Madefor Display", sans-serif;
}

span {
    display: block;
    font-weight: bold;
    font-size: 24px;
    margin-bottom: 20px;
    color: white;
    text-align: right;
    font-family: "Wix Madefor Display", sans-serif;
}

.warning-title {
    font-size: 32px;
    font-weight: bold;
    margin-bottom: 10px;
    text-align: center;
    color: white;
}

.delete-popup p {
    display: block;
    margin-bottom: 10px;
    font-weight: bold;
    font-size: 24px;
    color: white;
    font-family: "Wix Madefor Display", sans-serif;
}    

.close-button, .cancel-button, .confirm-delete-button {
    padding: 15px 30px;
    margin-top: 30px;
    border: none;
    border-radius: 3px;
    cursor: pointer;
    font-size: 16px;
    font-weight: bold;
    font-family: "Wix Madefor Display", sans-serif;
}

.button-group {
    display: flex;
    justify-content: space-between;
}

.close-button,
.cancel-button {
    background-color: #25262B;
    color: white;
    border: 2px solid white;
}

.confirm-delete-button {
    background-color: white;
    color: #25262B;
}
</style>

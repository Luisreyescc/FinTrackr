<template>
  <div class="user-row">
    <div class="user-icon">
      <font-awesome-icon :icon="['fas', 'user-tie']" class="row-icon"/>
    </div>
    
    <div class="user-details">
      <h4>{{ user.user_name }}</h4>
      <p class="user-fullname">{{ formattedFullname }}</p>
      <span v-if="user.birth_date" class="user-bday">{{ formattedBDate }}</span>
    </div>
    
    <div class="user-actions-section">
      <span class="user-network">{{ formattedNetwork }}</span>
      <div class="user-actions">
        <button class="full-button" @click="showFullData">
          <font-awesome-icon :icon="['fas', 'circle-info']" class="edit-icon" />
        </button>
        <button class="delete-button" @click="showDeleteWarning">
          <font-awesome-icon :icon="['fas', 'trash-can']" class="trash-icon" />
        </button>
      </div>
    </div>
    
    <div v-if="isFullData" class="overlay" @click="cancelFullData"></div>
    <div v-if="isFullData" class="data-popup">
      <h3 class="user-title">{{ user.user_name }}</h3>
      <div class="popup-content">
        <label>Fullname:</label><span>{{ formattedFullname }}</span>
        <label>Email:</label><span>{{ user.email }}</span>
        <label>CURP:</label><span>{{ user.curp }}</span>
        <label>RFC:</label><span>{{ user.rfc }}</span>
        <label>Phone Number:</label><span>{{ user.phone }}</span>
        <label v-if="user.birth_date">Birth Date:</label><span v-if="user.birth_date">{{ formattedBDate }}</span>
        <label>Incomes:</label><span>{{ formattedCurrency(user.incomes) }}</span>
        <label>Expenses:</label><span>{{ formattedCurrency(user.expenses) }}</span>
        <label>Debts:</label><span>{{ formattedCurrency(user.debts) }}</span>
        <label>Network:</label><span>{{ formattedCurrency(user.network) }}</span>
        <button type="button" class="close-button" @click="cancelFullData">Close</button>
      </div>
    </div>

    <div v-if="showDeletePopup" class="overlay" @click="cancelDelete"></div>
    <div v-if="showDeletePopup" class="delete-popup">
      <h3 class="warning-title">Warning</h3>
      <p>This action is permanent and cannot be undone. Are you sure you want to delete this user?</p>
      <div class="popup-actions">
        <button class="cancel-button" @click="cancelDelete">Cancel</button>
        <button class="confirm-delete-button" @click="confirmDelete">Delete</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'UserRow',
  props: {
    //user: {
      //type: Object,
      //required: true
    //},
  },
  data() {
    return {
      user: {
        user_id: 1,
        user_name: "john_doe",
        name: "John",
        last_name: "Doe",
        email: "johndoe@example.com",
        curp: "JODO950101HDFLNN01",
        rfc: "JODO950101ABC",
        phone: "555-123-4567",
        birth_date: "1995-01-01",
        incomes: 50000,
        expenses: 20000,
        debts: 10000,
        network: 20000
      },
      isFullData: false,
      showDeletePopup: false
    };
  },
  computed: {
    formattedFullname() {
      return `${this.user.name} ${this.user.last_name}`;
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
    color: #D160DE;
    font-weight: bold;
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

.user-actions-section {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    margin-left: 25px;
    margin-top: 5px;
}

.user-network {
    font-weight: bold;
    color: #20C171;
    font-size: 20px;
    flex-shrink: 0;
}

.user-actions {
    display: flex;
    gap: 10px;
    margin-top: 15px;
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

.edit-icon {
    font-size: 20px;
    color: #25262B;
}

.trash-icon {
    font-size: 20px;
    color: white;
}

.overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.6);
    z-index: 1000;
}

.data-popup, .delete-popup {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background: #25262b;
    color: white;
    border-radius: 10px;
    padding: 20px;
    z-index: 1100;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.popup-content {
    display: grid;
    grid-template-columns: 150px auto;
    gap: 10px;
}

.close-button, .cancel-button, .confirm-delete-button {
    background: #d160de;
    border: none;
    color: white;
    padding: 10px 20px;
    cursor: pointer;
    border-radius: 5px;
    margin-top: 20px;
    align-self: center;
}

.cancel-button {
    background: #D55C5C;
}

.confirm-delete-button {
    background: #20C171;
}

.warning-title {
    font-size: 24px;
    font-weight: bold;
    margin-bottom: 10px;
    text-align: center;
    color: #D55C5C;
}
</style>

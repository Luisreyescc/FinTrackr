<template>
  <div class="user-row">
    <div class="user-icon">
      <font-awesome-icon :icon="['fas', 'user-tie']" class="row-icon"/>
    </div>
    
    <div class="user-details">
      <h4>{{ user.username }}</h4>
      <p class="user-fullname">{{ formattedFullname }}</p>
      <span class="user-bday">{{ formattedBDay }}</span>
    </div>
    
    <div class="user-actions-section">
      <span class="user-network">{{ formattedNetwork }}</span>
      <div class="user-data">
	<button class="full-button" @click="showFullData">
          <font-awesome-icon :icon="['fas', 'circle-info']" class="edit-icon" />
        </button>
      </div>
    </div>
    
    <div v-if="isFullData" class="overlay" @click="cancelFullData"></div>
    <div v-if="isFullData" class="data-popup">
      <h3 class="user-title">{{ user.username }}</h3>
      <div class="popup-content">
        <label>Fullname:</label><span>{{ formattedFullname }}</span>
        <label>Email:</label><span>{{ user.email }}</span>
        <label>CURP:</label><span>{{ user.curp }}</span>
        <label>RFC:</label><span>{{ user.rfc }}</span>
        <label>Phone Number:</label><span>{{ user.phone }}</span>
        <label>Password:</label><span>{{ user.password }}</span>
        <label>Network:</label><span>{{ formattedNetwork }}</span>
        <label>Incomes:</label><span>{{ formattedCurrency(user.incomes) }}</span>
        <label>Expenses:</label><span>{{ formattedCurrency(user.expenses) }}</span>
        <label>Debts:</label><span>{{ formattedCurrency(user.debts) }}</span>
        <button type="button" class="close-button" @click="cancelFullData">Close</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'UserRow',
  props: {
    user: {
      type: Object,
      required: true
    },
  },
  data() {
    return {
      isFullData: false
    };
  },
  computed: {
    formattedFullname() {
      return `${this.user.name} ${this.user.last_name}`;
    },
    formattedNetwork() {
      return this.formattedCurrency(this.user.network);
    },
    formattedBDate() {
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
      return formatter.format(amount);
    },
    showFullData() {
      this.isFullData = true;
    },
    cancelFullData() {
      this.isFullData = false;
    },
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
    color: #20C171;
}

.full-button {
    background: none;
    border: none;
    cursor: pointer;
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

.data-popup {
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

.close-button {
    background: #d160de;
    border: none;
    color: white;
    padding: 10px 20px;
    cursor: pointer;
    border-radius: 5px;
    margin-top: 20px;
    align-self: center;
}
</style>

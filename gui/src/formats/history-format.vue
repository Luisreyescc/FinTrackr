<template>
<div class="history-form">
  <div class="sidebar">
    <button @click="toggleSidebar" class="menu-button">
      <font-awesome-icon :icon="['fas', 'bars']" font-size="32"/>
    </button>
  </div>
  
  <div class="content-wrapper">
    <div v-if="selectedContent === 'History'" class="main-content">
      <div class="events-container">
        <div class="header">
          <h2 class="section-title">Your History</h2>
          <HistoryHeader @resetClicked="handleResetClick" @search="handleSearch"/>
        </div>
        <div class="activity-content">
          <h3 class="activity-title">Activity</h3>
          <div class="activity-section">
            <div class="list-container scrollbar">
              <EventRow
                v-for="(event, index) in sortedEvent"
                :key="index"
                :event="event"/>
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
import moment from 'moment';
import '@/css/scrollbar.css';
import MessageAlerts from '@/components/messages.vue';

import HistoryHeader from '@/events/history-header.vue';
import EventRow from '@/events/row-event.vue';

export default {
  name: "HomeForm",
  components: {
    HistoryHeader,
    EventRow,
    MessageAlerts
  },
  props: {
    selectedContent: {
      type: String,
      default: 'History',
    },
  },
  data() {
    return {
      event: [],
      messages: []
    };
  },
  computed: {
    sortedEvent() {
      return this.event.slice().sort((a, b) => new Date(b.date) - new Date(a.date));
    },
  },
  methods: {
    formatDate(date) {
      return moment(date).format("MMM DD, YYYY");
    },
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
    async fetchIncomes() {
      try {
        const token = localStorage.getItem("token");
        if (!token) return console.error("No token found");

        const response = await axios.get('http://localhost:8000/api/incomes/', {
          headers: { Authorization: `Bearer ${token}` },
        });
        const incomes =
              response.data.map((income) => ({
		...income,
		date: this.formatDate(income.date),
              }));
        this.event.push(...incomes);
      } catch (error) {
        console.error('Error fetching incomes:', error);
        this.addMessage("There was an error fetching your incomes.", "error");
      }
    },
    async fetchExpenses() {
      try {
        const token = localStorage.getItem("token");
        if (!token) return console.error("No token found");

        const response = await axios.get('http://localhost:8000/api/expenses/', {
          headers: { Authorization: `Bearer ${token}` },
        });
        const expenses =
              response.data.map((expense) => ({
		...expense,
		date: this.formatDate(expense.date),
              }));
	
        this.event.push(...expenses);
      } catch (error) {
        console.error('Error fetching expenses:', error);
        this.addMessage("There was an error fetching your expenses.", "error");
      }
    },
    async fetchDebts() {
      try {
        const token = localStorage.getItem("token");
        if (!token) return console.error("No token found");

        const response = await axios.get('http://localhost:8000/api/debts/', {
          headers: { Authorization: `Bearer ${token}` },
        });
        const debts =
              response.data.map((debt) => ({
		...debt,
		date: this.formatDate(debt.date),
              }));
	this.event.push(...debts);
      } catch (error) {
        console.error('Error fetching debts:', error);
        this.addMessage("There was an error fetching your debts.", "error");
      }
    },
    handleResetClick() {
      this.addMessage("Reset button clicked!", "neutral");
      console.log("Clock button clicked");
    },
    handleSearch(query) {
      console.log("Search query:", query);
      this.addMessage("Searching: ", "neutral");
    },
  },
  mounted() {
    if (this.selectedContent === "History") {
      this.fetchIncomes();
      this.fetchExpenses();
      this.fetchDebts();
    }
  },
  watch: {
    selectedContent(newValue) {
      if (newValue === "History") {
        this.fetchIncomes();
	this.fetchExpenses();
        this.fetchDebts();
      }
    }
  },
};
</script>

<style scoped>
.history-form {
    display: flex;
    width: 100%;
    overflow: hidden;
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
    padding: 15px;
    margin-top: -15px;
    margin-left: 5px;
    background: none;
    border: none;
    cursor: pointer;
    color: #25253C;
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
    border-radius: 8px;
    box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
    background-color: #fff;
    overflow: hidden;
}

.header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-family: "Wix Madefor Display", sans-serif;
    padding: 10px 20px;
    border-bottom: 1px solid #ddd;
}

.header h3 {
    font-size: 32px; 
}

.section-title {
    font-size: 32px;
    font-weight: bold;
    color: #141428;
    font-family: "Wix Madefor Display", sans-serif;
}

.activity-content {
    display: flex;
    flex-direction: column;
    max-height: 100vh;
    overflow: hidden;
    padding: 20px;
    border-top: 1px solid #eee;
    position: relative;
}

.activity-title {
    font-size: 28px;
    font-weight: bold;
    margin-bottom: 10px;
    text-align: left;
    color: #141428;
    font-family: "Wix Madefor Display", sans-serif;
}

.list-container {
    flex: 1;
    overflow-y: auto;
    padding-right: 10px;
    max-height: calc(70vh - 50px);
}

.forms-section {
    position: fixed;
    right: 0;
    top: 100px;
    bottom: 40px;
    width: 450px;
    max-width: 100%;
    padding: 20px;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    background: #ffffff;
    border-radius: 9px;
    box-shadow: -2px 0 8px rgba(0, 0, 0, 0.2);
    transition: transform 0.3s ease;
    z-index: 1001;
}

.forms-section-enter-active, .forms-section-leave-active {
    transition: transform 0.3s ease;
}

.forms-section-enter {
    transform: translateX(100%);
}

.forms-section-leave-to {
    transform: translateX(100%);
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
</style>

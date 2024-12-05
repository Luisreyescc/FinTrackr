<template>
<div class="history-form">
  <div class="sidebar">
    <button @click="toggleSidebar" class="menu-button">
      <font-awesome-icon :icon="['fas', 'bars']" font-size="38"/>
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
              <span v-if="loadingEvents">Loading events...</span>
              <EventRow v-for="(event, index) in filteredEvents" :key="index" :event="event"/>
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
  name: "HistoryForm",
  components: {
    HistoryHeader,
    EventRow,
    MessageAlerts
  },
  props: {
    selectedContent: {
      type: String,
      default: 'History'
    },
  },
  data() {
    return {
      event: [],
      messages: [],
      searchQuery: "",
      loadingEvents: false
    };
  },
  computed: {
    sortedEvent() {
      return this.event.slice().sort((a, b) => {
        const dateA = new Date(a.date);
        const dateB = new Date(b.date);
        if (dateA > dateB)
          return -1;
        if (dateA < dateB)
          return 1;
        // If dates are equal, sort by type
        const typeOrder = { 'Income': 1, 'Expense': 2, 'Debt': 3 };
        return typeOrder[a.type] - typeOrder[b.type];
      });
    },
    filteredEvents() {
      let events = this.sortedEvent;

      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase();
        const [filterType, filterValue] = query.includes(':') ? query.split(':').map(s => s.trim()) : [null, query];

        if (filterValue) {
          if (filterType === 'amount ==') {
            const amount = parseFloat(filterValue);
            events = events.filter(event => Math.abs(event.amount) === amount);
          } else if (filterType === 'amount >=') {
            const amount = parseFloat(filterValue);
            events = events.filter(event => event.amount >= amount);
          } else if (filterType === 'amount <=') {
            const amount = parseFloat(filterValue);
            events = events.filter(event => event.amount <= amount);
          } else if (filterType === 'date') {
            const dateFormats = ["YYYY-MM-DD", "YYYY-MMM-DD", "YYYY-MM", "YYYY-MMM", "YYYY"];
            events = events.filter(event => {
              return dateFormats.some(format => {
                const eventDate = moment(event.date, "YYYY-MMM-DD");
                const filterDate = moment(filterValue, format);
                if (filterValue.length === 4) {
                  return eventDate.isSame(filterDate, 'year');
                } else if (filterValue.length === 7 || filterValue.length === 8) {
                  return eventDate.isSame(filterDate, 'month');
                } else {
                  return eventDate.isSame(filterDate, 'day');
                }
              });
            });
          } else if (filterType === 'category') {
            events = events.filter(event => event.categories.some(category => category.toLowerCase().startsWith(filterValue.toLowerCase())));
          } else if (filterType === 'description') {
            events = events.filter(event => event.description.toLowerCase().includes(filterValue.toLowerCase()));
          } else {
            // Global search
            const dateFormats = ["YYYY-MM-DD", "YYYY-MMM-DD", "YYYY-MM", "YYYY-MMM", "YYYY"];
            const amount = parseFloat(filterValue);
            events = events.filter(event => {
              return (
                event.description.toLowerCase().includes(filterValue) ||
                event.categories.some(category => category.toLowerCase().includes(filterValue)) ||
                dateFormats.some(format => moment(event.date, "YYYY-MMM-DD").isSame(moment(filterValue, format), 'day')) ||
                (!isNaN(amount) && Math.abs(event.amount) === amount)
              );
            });
          }
        }
      }

      return events;
    }
  },
  methods: {
    formatDate(date) {
      return moment(date).format("YYYY-MMM-DD");
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
        if (!token)
          return console.error("No token found");

	this.loadingEvents = true;
        const response = await axios.get('http://localhost:8000/api/incomes/', {
          headers: { Authorization: `Bearer ${token}` },
        });
        const incomes = response.data.map((income) => ({
          ...income,
          date: this.formatDate(income.date),
          type: 'Income' // Add type field
        }));
        this.event.push(...incomes);
      } catch (error) {
        console.error('Error fetching incomes:', error);
        this.addMessage("There was an error fetching your incomes.", "error");
      } finally {
	this.loadingEvents = false;
      }
    },
    async fetchExpenses() {
      try {
        const token = localStorage.getItem("token");
        if (!token)
          return console.error("No token found");

	this.loadingEvents = true;
        const response = await axios.get('http://localhost:8000/api/expenses/', {
          headers: { Authorization: `Bearer ${token}` },
        });
        const expenses = response.data.map((expense) => ({
          ...expense,
          date: this.formatDate(expense.date),
          type: 'Expense' // Add type field
        }));
        this.event.push(...expenses);
      } catch (error) {
        console.error('Error fetching expenses:', error);
        this.addMessage("There was an error fetching your expenses.", "error");
      } finally {
	this.loadingEvents = false;
      }
    },
    async fetchDebts() {
      try {
        const token = localStorage.getItem("token");
        if (!token)
          return console.error("No token found");

	this.loadingEvents = true;
        const response = await axios.get('http://localhost:8000/api/debts/', {
          headers: { Authorization: `Bearer ${token}` },
        });
        const debts = response.data.map((debt) => ({
          ...debt,
          date: this.formatDate(debt.date),
          type: 'Debt' // Add type field
        }));
        this.event.push(...debts);
      } catch (error) {
        console.error('Error fetching debts:', error);
        this.addMessage("There was an error fetching your debts.", "error");
      } finally {
	this.loadingEvents = false;
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

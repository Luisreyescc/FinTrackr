<template>
<div class="home-form">
  <div class="sidebar">
    <button @click="toggleSidebar" class="menu-button">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512" width="32" height="32">
	<path d="M0 96C0 78.3 14.3 64 32 64l384 0c17.7 0 32 14.3 32 32s-14.3 32-32 32L32 128C14.3 128 0 113.7 0 96zM0 256c0-17.7 14.3-32 32-32l384 0c17.7 0 32 14.3 32 32s-14.3 32-32 32L32 288c-17.7 0-32-14.3-32-32zM448 416c0 17.7-14.3 32-32 32L32 448c-17.7 0-32-14.3-32-32s14.3-32 32-32l384 0c17.7 0 32 14.3 32 32z"/>
      </svg>
    </button>
  </div>
  
  <div class="content-wrapper">
    <div v-if="selectedContent === 'Incomes'" class="main-content">
      <div class="incomes-container">
	<div class="header">
          <h2 class="section-title">{{ selectedContent }}</h2><IncomeButton @click="toggleForm" />
	</div>
	<div class="activity-content"><h3 class="activity-title">Activity</h3>
          <div class="activity-section">
            <div class="list-container">
              <IncomeRow v-for="(income, index) in incomes" :key="index" :income="income" />
            </div>
          </div>
	</div>
      </div>
      <div class="forms-section" v-if="showForm">
	<IncomesForm @submitForm="handleIncomeSubmission" @closeForm="toggleForm" />
      </div>
    </div>
  
   <div v-if="selectedContent === 'Expenses'" class="main-content">
     <div class="expenses-containert">
       <div class="header">
	<h2 class="section-title">{{ selectedContent }}</h2>
	<ExpenseButton @click="toggleForm" />
       </div>
       <div class="activity-content">
	<h3 class="activity-title">Activity</h3>
         <div class="activity-section"><div class="list-container"><ExpenseRow v-for="(expense, index) in expenses" :key="index" :expense="expense" />
           </div>
	</div>
       </div>
     </div>
     <div class="forms-section" v-if="showForm">
       <ExpensesForm @submitForm="handleExpenseSubmission"  @closeForm="toggleForm"/>
     </div>
   </div>
  </div>
</div>

</template>

<script>
import axios from 'axios';
import IncomesForm from '@/components/incomes-forms.vue';
import IncomeButton from '@/components/incomes-header.vue';
import IncomeRow from '@/components/income-row.vue';

import ExpensesForm from '@/components/expenses/expenses-forms.vue';
import ExpenseButton from '@/components/expenses/expenses-header.vue';
import ExpenseRow from '@/components/expenses/expense-row.vue';

export default {
  name: "HomeForm",
  components: {
    IncomesForm,
    IncomeButton,
    IncomeRow,
    ExpensesForm,
    ExpenseButton,
    ExpenseRow,
  },
  props: {
    selectedContent: {
      type: String,
      default: 'Incomes',
    },
  },
  data() {
    return {
      showForm: false,
      incomes: [],
      expenses: [],
    };
  },
  methods: {
    toggleSidebar() {
      this.$emit('toggleSidebar');
    },
    toggleForm() {
      this.showForm = !this.showForm;
    },
    async fetchIncomes() {
      try {
        const token = localStorage.getItem("token");
        if (!token) return console.error("No token found");
        
        const response = await axios.get('http://localhost:8000/api/incomes/', {
          headers: { Authorization: `Bearer ${token}` },
        });
        this.incomes = response.data;
      } catch (error) {
        console.error('Error fetching incomes:', error);
      }
    },
    async fetchExpenses() {
      try {
        const token = localStorage.getItem("token");
        if (!token) return console.error("No token found");

        const response = await axios.get('http://localhost:8000/api/expenses/', {
          headers: { Authorization: `Bearer ${token}` },
        });
        this.expenses = response.data;
      } catch (error) {
        console.error('Error fetching expenses:', error);
      }
    },
    async handleIncomeSubmission(incomeData) {
      try {
        const token = localStorage.getItem("token");
        if (!token) return console.error("No token found");

        const response = await axios.post(
          'http://localhost:8000/api/incomes/',
          incomeData,
          { headers: { Authorization: `Bearer ${token}` } }
        );
        this.incomes.push(response.data);
        this.showForm = false;
      } catch (error) {
        console.error('Error submitting income:', error);
      }
    },
    async handleExpenseSubmission(expenseData) {
      try {
        const token = localStorage.getItem("token");
        if (!token) return console.error("No token found");

        const response = await axios.post(
          'http://localhost:8000/api/expenses/',
          expenseData,
          { headers: { Authorization: `Bearer ${token}` } }
        );
        this.expenses.push(response.data);
        this.showForm = false;
      } catch (error) {
        console.error('Error submitting expense:', error);
      }
    },
  },
  mounted() {
    if (this.selectedContent === "Incomes") {
      this.fetchIncomes();
    } else if (this.selectedContent === "Expenses") {
      this.fetchExpenses();
    }
  },
};
</script>

<style scoped>
.home-form {
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
    background: none;
    border: none;
    cursor: pointer;
    transition: transform 0.2s ease-in-out;
    padding: 15px;
    margin-top: -15px;
    margin-left: 5px;
}

.menu-button svg {
    fill: #21255B;
    transition: transform 0.2s ease-in-out;
}

.menu-button svg:hover {
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
    max-width: 800px;
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

.section-title {
    font-size: 24px;
    font-weight: bold;
    color: #333;
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
    font-size: 20px;
    font-weight: bold;
    margin-bottom: 10px;
    text-align: left;
    font-family: "Wix Madefor Display", sans-serif;
}

.list-container {
    flex: 1;
    overflow-y: auto;
    padding-right: 10px;
    max-height: calc(70vh - 50px);
    scrollbar-width: thin;
    scrollbar-color: #00A0BE #e0e0e0;
}

.forms-section {
  position: fixed;
  right: 0;
  top: 100px;
  bottom: 200px;
  width: 450px;
  max-width: 100%;
  padding: 20px;
  background: #ffffff;
  border-radius: 9px;
  box-shadow: -2px 0 8px rgba(0, 0, 0, 0.2);
  transition: transform 0.3s ease;
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
</style>

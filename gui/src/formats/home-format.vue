<template>
<div class="home-form">
  <div class="sidebar">
    <button @click="toggleSidebar" class="menu-button">
	<font-awesome-icon :icon="['fas', 'bars']" font-size="32"/>
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
              <IncomeRow v-for="(income, index) in sortedIncomes" :key="index" :income="income" @updateIncome="handleIncomeUpdate" @deleteIncome="handleIncomeDelete"/>
            </div>
          </div>
	</div>
      </div>
      <div v-if="showForm" class="overlay" @click="toggleForm"></div>
      <div class="forms-section" v-if="showForm">
	<IncomesForm @submitForm="handleIncomeSubmission" @closeForm="toggleForm" />
      </div>
    </div>
  
   <div v-if="selectedContent === 'Expenses'" class="main-content">
     <div class="expenses-container">
       <div class="header">
	<h2 class="section-title">{{ selectedContent }}</h2>
	<ExpenseButton @click="toggleForm" />
       </div>
       <div class="activity-content">
	<h3 class="activity-title">Activity</h3>
        <div class="activity-section"><div class="list-container">
	<ExpenseRow v-for="(expense, index) in sortedExpenses" :key="index" :expense="expense" @updateExpense="handleExpenseUpdate" @deleteIncome="handleExpenseDelete"/>
           </div>
	</div>
       </div>
     </div>
     <div v-if="showForm" class="overlay" @click="toggleForm"></div>
     <div class="forms-section" v-if="showForm">
       <ExpensesForm @submitForm="handleExpenseSubmission"  @closeForm="toggleForm"/>
     </div>
   </div>
  </div>
</div>
</template>

<script>
import axios from 'axios';

import IncomesForm from '@/components/incomes/incomes-forms.vue';
import IncomeButton from '@/components/incomes/incomes-header.vue';
import IncomeRow from '@/components/incomes/income-row.vue';
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
  computed: {
    sortedIncomes() {
      return this.incomes.slice().sort((a, b) => new Date(b.date) - new Date(a.date));
    },
    sortedExpenses() {
      return this.expenses.slice().sort((a, b) => new Date(b.date) - new Date(a.date));
    },
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
        this.incomes.unshift(response.data);
        this.showForm = false;
      } catch (error) {
        console.error('Error submitting income:', error);
      }
    },
    async handleExpenseSubmission(expenseData) {
      try {
        const token = localStorage.getItem("token");
        const userId = localStorage.getItem("user_id") ?? 1;
        const modifiedExpenseData = {
          ...expenseData,
          user: userId,
          category: expenseData.categories,
        };
        delete modifiedExpenseData.categories;

        const response = await axios.post(
          'http://localhost:8000/api/expenses/',
          modifiedExpenseData,
          { headers: { Authorization: `Bearer ${token}` } }
        );

        this.expenses.push(response.data);
        this.showForm = false;
      } catch (error) {
        console.error('Error submitting expense:', error.response?.data || error.message);
      }
    },
    async handleIncomeUpdate(updatedIncome) {
      try {
	const token = localStorage.getItem("token");
	await axios.put(
          `http://localhost:8000/api/incomes/${updatedIncome.id}/`,
          updatedIncome,
          { headers: { Authorization: `Bearer ${token}` } }
	);
	// We update the income in the local array
	const index = this.incomes.findIndex((income) => income.id === updatedIncome.id);
	if (index !== -1) {
        this.$set(this.incomes, index, updatedIncome); // Replace content
	}
      } catch (error) {
	console.error("Error updating income:", error);
      }
    },
    async handleIncomeDelete(incomeId) {
      try {
	const token = localStorage.getItem("token");
	await axios.delete(`http://localhost:8000/api/incomes/${incomeId}/`, {
          headers: { Authorization: `Bearer ${token}` },
	});
	
	this.incomes = this.incomes.filter((income) => income.id !== incomeId);
      } catch (error) {
	console.error("Error deleting income:", error);
      }
    },
    async handleExpenseUpdate(updatedExpense) {
      try {
	const token = localStorage.getItem("token");
	await axios.put(
          `http://localhost:8000/api/expenses/${updatedExpense.id}/`,
          updatedExpense,
          { headers: { Authorization: `Bearer ${token}` } }
	);
	// We update the income in the local array
	const index = this.expense.findIndex((expense) => expense.id === updatedExpense.id);
	if (index !== -1) {
        this.$set(this.expense, index, updatedExpense); // Replace content
	}
      } catch (error) {
	console.error("Error updating expense:", error);
      }
    },
    async handleExpenseDelete(expenseId) {
      try {
	const token = localStorage.getItem("token");
	await axios.delete(`http://localhost:8000/api/expenses/${expenseId}/`, {
          headers: { Authorization: `Bearer ${token}` },
	});
	
	this.expense = this.expense.filter((expense) => expense.id !== expenseId);
      } catch (error) {
	console.error("Error deleting expense:", error);
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
  watch: {
    selectedContent(newValue) {
      if (newValue === "Incomes") {
        this.fetchIncomes();
      } else if (newValue === "Expenses") {
        this.fetchExpenses();
      }
    }
  }
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

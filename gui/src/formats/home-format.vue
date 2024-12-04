<template>
  <div class="home-form">
    <div class="sidebar">
      <button @click="toggleSidebar" class="menu-button">
        <font-awesome-icon :icon="['fas', 'bars']" font-size="38"/>
      </button>
    </div>
    
    <div class="content-wrapper">
      <div v-if="selectedContent === 'Incomes'" class="main-content">
        <div class="incomes-container">
          <div class="header">
            <h2 class="section-title">{{ selectedContent }}</h2>
            <SearchBar @search="handleSearch"/>
            <IncomeButton @click="toggleForm"/>
          </div>
          <div class="activity-content">
            <h3 class="activity-title">Activity</h3>
            <div class="activity-section">
              <div class="list-container scrollbar">
                <IncomeRow
                  v-for="(income, index) in filteredIncomes"
                  :key="index"
                  :income="income"
                  @updateIncome="handleIncomeUpdate"
                  @deleteIncome="handleIncomeDelete"/>
              </div>
            </div>
          </div>
        </div>
        <div v-if="showForm" class="overlay" @click="toggleForm"></div>
        <div class="forms-section" v-if="showForm">
          <IncomesForm @submitForm="handleIncomeSubmission" @closeForm="toggleForm"/>
        </div>
      </div>
      
      <div v-if="selectedContent === 'Expenses'" class="main-content">
        <div class="expenses-container">
          <div class="header">
            <h2 class="section-title">{{ selectedContent }}</h2>
            <SearchBar @search="handleSearch" />
            <ExpenseButton @click="toggleForm"/>
          </div>
          <div class="activity-content scrollbar">
            <h3 class="activity-title">Activity</h3>
            <div class="activity-section">
              <div class="list-container scrollbar">
                <ExpenseRow
                  v-for="(expense, index) in filteredExpenses"
                  :key="index"
                  :expense="expense"
                  @updateExpense="handleExpenseUpdate"
                  @deleteExpense="handleExpenseDelete"/>
              </div>
            </div>
          </div>
        </div>
        <div v-if="showForm" class="overlay" @click="toggleForm"></div>
        <div class="forms-section" v-if="showForm">
          <ExpensesForm @submitForm="handleExpenseSubmission" @closeForm="toggleForm"/>
        </div>
      </div>

      <div v-if="selectedContent === 'Debts'" class="main-content">
        <div class="debts-container">
          <div class="header">
            <h2 class="section-title">{{ selectedContent }}</h2>
            <SearchBar @search="handleSearch" />
            <DebtButton @click="toggleForm"/>
          </div>
          <div class="activity-content scrollbar">
            <h3 class="activity-title">Activity</h3>
            <div class="activity-section">
              <div class="list-container scrollbar">
                <DebtRow
                  v-for="(debt, index) in filteredDebts"
                  :key="index"
                  :debt="debt"
                  @updateDebt="handleDebtUpdate"
                  @deleteDebt="handleDebtDelete"/>
              </div>
            </div>
          </div>
        </div>
        <div v-if="showForm" class="overlay" @click="toggleForm"></div>
        <div class="forms-section" v-if="showForm">
          <DebtsForm @submitForm="handleDebtSubmission" @closeForm="toggleForm"/>
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
  </div>
</template>

<script>
import axios from "axios";
import moment from "moment";
import "@/css/scrollbar.css";
import MessageAlerts from "@/components/messages.vue";

import IncomesForm from '@/events/incomes/incomes-forms.vue';
import IncomeButton from '@/events/incomes/incomes-header.vue';
import IncomeRow from '@/events/incomes/income-row.vue';
import ExpensesForm from '@/events/expenses/expenses-forms.vue';
import ExpenseButton from '@/events/expenses/expenses-header.vue';
import ExpenseRow from '@/events/expenses/expense-row.vue';
import DebtsForm from '@/events/debts/debts-forms.vue';
import DebtButton from '@/events/debts/debts-header.vue';
import DebtRow from '@/events/debts/debt-row.vue';
import SearchBar from '@/components/search-bar.vue';

export default {
  name: "HomeForm",
  components: {
    IncomesForm,
    IncomeButton,
    IncomeRow,
    ExpensesForm,
    ExpenseButton,
    ExpenseRow,
    DebtsForm,
    DebtButton,
    DebtRow,
    MessageAlerts,
    SearchBar
  },
  props: {
    selectedContent: {
      type: String,
      default: "Incomes"
    },
  },
  data() {
    return {
      showForm: false,
      incomes: [],
      expenses: [],
      debts: [],
      messages: [],
      searchQuery: ""
    };
  },
  computed: {
    filteredIncomes() {
      return this.sortedIncomes.filter(income => this.filterEvents(income));
    },
    filteredExpenses() {
      return this.sortedExpenses.filter(expense => this.filterEvents(expense));
    },
    filteredDebts() {
      return this.sortedDebts.filter(debt => this.filterEvents(debt));
    },
    sortedIncomes() {
      return this.incomes.slice().sort((a, b) => new Date(b.date) - new Date(a.date));
    },
    sortedExpenses() {
      return this.expenses.slice().sort((a, b) => new Date(b.date) - new Date(a.date));
    },
    sortedDebts() {
      return this.debts.slice().sort((a, b) => new Date(b.date) - new Date(a.date));
    }
  },
  methods: {
    handleSearch(query) {
      this.searchQuery = query;
    },
    filterEvents(event) {
      const searchQuery = this.searchQuery.toLowerCase();
      const dateFormats = ["YYYY-MM-DD", "YYYY-MMM-DD", "YYYY-MM", "YYYY-MMM", "YYYY"];
      const amount = parseFloat(searchQuery);

      return (
        event.amount?.toString().toLowerCase().includes(searchQuery) ||
        event.description?.toLowerCase().includes(searchQuery) ||
        event.categories?.some(category => category.toLowerCase().includes(searchQuery)) ||
        event.date?.toLowerCase().includes(searchQuery) ||
        dateFormats.some(format => {
          const eventDate = moment(event.date, "YYYY-MMM-DD");
          const filterDate = moment(searchQuery, format);
          if (searchQuery.length === 4) {
            return eventDate.isSame(filterDate, 'year');
          } else if (searchQuery.length === 7 || searchQuery.length === 8) {
            return eventDate.isSame(filterDate, 'month');
          } else {
            return eventDate.isSame(filterDate, 'day');
          }
        }) ||
        (!isNaN(amount) && Math.abs(event.amount) === amount)
      );
    },
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
      this.$emit("toggleSidebar");
    },
    toggleForm() {
      this.showForm = !this.showForm;
    },
    async fetchIncomes() {
      try {
        const token = localStorage.getItem("token");
        if (!token)
          return console.error("No token found");

        const response = await axios.get("http://localhost:8000/api/incomes/", {
          headers: { Authorization: `Bearer ${token}` } });
        this.incomes = response.data.map((income) => ({
          ...income,
          date: this.formatDate(income.date),
        }));
        console.log(this.incomes);
      } catch (error) {
        console.error("Error fetching incomes:", error);
        this.addMessage("There was an error fetching your incomes.", "error");
      }
    },
    async fetchExpenses() {
      try {
        const token = localStorage.getItem("token");
        if (!token)
          return console.error("No token found");

        const response = await axios.get(
          "http://localhost:8000/api/expenses/",
          {
            headers: { Authorization: `Bearer ${token}` },
          },
        );
        this.expenses = response.data.map((expense) => ({
          ...expense,
          date: this.formatDate(expense.date),
        }));
        console.log(this.expenses);
      } catch (error) {
        console.error("Error fetching expenses:", error);
        this.addMessage("There was an error fetching your expenses.", "error");
      }
    },
    async fetchDebts() {
      try {
        const token = localStorage.getItem("token");
        if (!token)
          return console.error("No token found");

        const response = await axios.get("http://localhost:8000/api/debts/", {
          headers: { Authorization: `Bearer ${token}` },
        });
        this.debts = response.data.map((debt) => ({
          ...debt,
          date: this.formatDate(debt.date),
        }));
        console.log(this.debts);
      } catch (error) {
        console.error("Error fetching debts:", error);
        this.addMessage("There was an error fetching your debts.", "error");
      }
    },
    async handleIncomeSubmission(incomeData) {
      try {
        const token = localStorage.getItem("token");
        const userId = localStorage.getItem("user_id") ?? 1;
        const modifiedIncomeData = {
          ...incomeData,
          user: userId,
          category: incomeData.categories,
        };
        delete modifiedIncomeData.categories;

        const response = await axios.post(
          "http://localhost:8000/api/incomes/",
          modifiedIncomeData,
          { headers: { Authorization: `Bearer ${token}` } },
        );
        this.incomes.unshift(response.data);
        this.showForm = false;
        this.fetchIncomes();
        this.addMessage("New income added succesfully.", "success");
      } catch (error) {
        console.error("Error submitting income:", error);
        this.addMessage("There was an error while adding the income.", "error");
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
          "http://localhost:8000/api/expenses/",
          modifiedExpenseData,
          { headers: { Authorization: `Bearer ${token}` } },
        );

        this.expenses.push(response.data);
        this.showForm = false;
        this.fetchExpenses();
        this.addMessage("New expense added succesfully.", "success");
      } catch (error) {
        console.error(
          "Error submitting expense:",
          error.response?.data || error.message,
        );
        this.addMessage(
          "There was an error while adding the expense.",
          "error",
        );
      }
    },
    async handleDebtSubmission(debtData) {
      try {
        const token = localStorage.getItem("token");
        const userId = localStorage.getItem("user_id") ?? 1;
        const modifiedDebtData = {
          ...debtData,
          user: userId,
          category: debtData.categories,
        };
        delete modifiedDebtData.categories;

        const response = await axios.post(
          "http://localhost:8000/api/debts/",
          modifiedDebtData,
          { headers: { Authorization: `Bearer ${token}` } },
        );

        this.debts.push(response.data);
        this.showForm = false;
        this.fetchDebts();
        this.addMessage("New debt added succesfully.", "success");
      } catch (error) {
        console.error(
          "Error submitting debt:",
          error.response?.data || error.message,
        );
        this.addMessage("There was an error while adding the debt.", "error");
      }
    },
    async handleIncomeUpdate(updatedIncome) {
      try {
        const token = localStorage.getItem("token");
        const modifiedIncomeData = {
          ...updatedIncome,
          category: [...updatedIncome.categories],
        };
        delete modifiedIncomeData.categories;

        const response = await axios.put(
          `http://localhost:8000/api/incomes/${updatedIncome.income_id}/`,
          modifiedIncomeData,
          { headers: { Authorization: `Bearer ${token}` } },
        );

        if (response.status === 200) {
          const index = this.incomes.findIndex(
            (income) => income.income_id === updatedIncome.income_id,
          );
          if (index !== -1) {
            this.incomes[index] = response.data;
            this.fetchIncomes();
          }
          this.addMessage("Income data edited successfully.", "success");
        }

        this.fetchIncomes();
      } catch (error) {
        console.error("Error updating income:", error);
        this.addMessage(
          "There was an error while saving the income changes.",
          "error",
        );
      }
    },
    async handleIncomeDelete(incomeId) {
      try {
        const token = localStorage.getItem("token");
        const response = await axios.delete(
          `http://localhost:8000/api/incomes/${incomeId}/`,
          {
            headers: { Authorization: `Bearer ${token}` },
          },
        );
        if (response.status === 204) {
          console.log("Succes");
          this.fetchIncomes();
          this.incomes = this.incomes.filter(
            (income) => income.income_id !== incomeId,
          );
          this.addMessage("Income deleted successfully.", "success");
        }
      } catch (error) {
        console.error("Error deleting income:", error);
        this.addMessage(
          "There was an error while deleting the income.",
          "error",
        );
      }
    },
    async handleExpenseUpdate(updatedExpense) {
      try {
        const token = localStorage.getItem("token");
        const modifiedExpenseData = {
          ...updatedExpense,
          category: [...updatedExpense.categories], // Aseguramos que sea un array de strings
        };
        delete modifiedExpenseData.categories;

        const response = await axios.put(
          `http://localhost:8000/api/expenses/${updatedExpense.expense_id}/`,
          modifiedExpenseData,
          { headers: { Authorization: `Bearer ${token}` } },
        );

        if (response.status === 200) {
          const index = this.expenses.findIndex(
            (expense) => expense.expense_id === updatedExpense.expense_id,
          );
          if (index !== -1) {
            this.expenses[index] = response.data;
            this.fetchExpenses();
          }
          this.addMessage("Expense data edited successfully.", "success");
        }

        this.fetchExpenses();
      } catch (error) {
        console.error("Error updating expense:", error);
        this.addMessage(
          "There was an error while saving the expense changes.",
          "error",
        );
      }
    },
    async handleExpenseDelete(expenseId) {
      try {
        const token = localStorage.getItem("token");
        const response = await axios.delete(
          `http://localhost:8000/api/expenses/${expenseId}/`,
          {
            headers: { Authorization: `Bearer ${token}` },
          },
        );

        if (response.status === 204) {
          console.log("Success");
          this.fetchExpenses();
          this.expenses = this.expenses.filter(
            (expense) => expense.expense_id !== expenseId,
          );
          this.addMessage("Expense deleted successfully.", "success");
        }
      } catch (error) {
        console.error("Error deleting expense:", error);
        this.addMessage(
          "There was an error while deleting the expense.",
          "error",
        );
      }
    },
    async handleDebtUpdate(updatedDebt) {
      try {
        const token = localStorage.getItem("token");
        const modifiedDebtData = {
          ...updatedDebt,
          category: updatedDebt.categories,
        };
        delete modifiedDebtData.categories;

        const response = await axios.put(
          `http://localhost:8000/api/debts/${updatedDebt.debt_id}/`,
          modifiedDebtData,
          { headers: { Authorization: `Bearer ${token}` } },
        );

        if (response.status === 200) {
          const index = this.debts.findIndex(
            (debt) => debt.debt_id === updatedDebt.debt_id,
          );
          if (index !== -1) {
            this.debts[index] = response.data;
            this.fetchDebts();
          }
          this.addMessage("Debt data edited succesfully.", "success");
        }

        this.fetchDebts();
      } catch (error) {
        console.error("Error updating debt:", error);
        this.addMessage(
          "There was an error while saving the debt changes.",
          "error",
        );
      }
    },
    async handleDebtDelete(debtId) {
      try {
        const token = localStorage.getItem("token");
        const response = await axios.delete(
          `http://localhost:8000/api/debts/${debtId}/`,
          {
            headers: { Authorization: `Bearer ${token}` },
          },
        );

        if (response.status === 204) {
          this.fetchDebts();
          this.debts = this.debts.filter((debt) => debt.debt_id !== debtId);
          this.addMessage("Debt deleted successfully.", "success");
        }
      } catch (error) {
        console.error("Error deleting debt:", error);
        this.addMessage("There was an error while deleting the debt.", "error");
      }
    },
  },
  mounted() {
    if (this.selectedContent === "Incomes")
      this.fetchIncomes();
    else if (this.selectedContent === "Expenses")
      this.fetchExpenses();
    else if (this.selectedContent === "Debts")
      this.fetchDebts();
  },
  watch: {
    selectedContent(newValue) {
      if (newValue === "Incomes")
        this.fetchIncomes();
      else if (newValue === "Expenses")
        this.fetchExpenses();
      else if (newValue === "Debts")
        this.fetchDebts();
    }
  },
};
</script>

<style scoped>
.home-form {
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
    border-radius: 8px;
    border: 2px solid rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    box-shadow: 0 2px 10px rgba(255, 255, 255, 0.1);
    background: white;
}

.header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 10px 20px;
    background: white;
    border-radius: 12px;
    font-family: "Wix Madefor Display", sans-serif;
}

.header h3 {
    font-size: 32px;
}

.section-title {
    font-size: 32px;
    font-weight: bold;
    color: #25262B;
    font-family: "Wix Madefor Display", sans-serif;
}

.activity-content {
    display: flex;
    flex-direction: column;
    max-height: 100vh;
    overflow: hidden;
    padding: 20px;
    border-top: 1px solid #25262B;
    background: white;
    position: relative;
}

.activity-title {
    font-size: 28px;
    font-weight: bold;
    margin-bottom: 10px;
    text-align: left;
    color: #25262B;
    font-family: "Wix Madefor Display", sans-serif;
}

.list-container {
    flex: 1;
    overflow-y: auto;
    padding-right: 10px;
    border-radius: 12px;
    max-height: calc(70vh - 50px);
}

.forms-section {
    position: fixed;
    right: 0;
    top: 100px;
    bottom: 40px;
    width: 600px;
    max-width: 100%;
    padding: 20px;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    background: #25262B;
    border-radius: 12px;
    box-shadow: -2px 0 8px rgba(225, 225, 225, 0.1);
    transition: transform 0.3s ease;
    z-index: 1001;
}

.forms-section-enter-active,
.forms-section-leave-active {
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

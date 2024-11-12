<template>
<div class="home-form">
  <!-- Button to toggle the sidebar -->
  <button @click="$emit('toggleSidebar')" class="menu-button">
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 512" width="32" height="32">
      <path d="M278.6 233.4c12.5 12.5 12.5 32.8 0 45.3l-160 160c-12.5 12.5-32.8 12.5-45.3 0s-12.5-32.8 0-45.3L210.7 256 73.4 118.6c-12.5-12.5-12.5-32.8 0-45.3s32.8-12.5 45.3 0l160 160z"/>
    </svg>
  </button>

    <div v-if="selectedContent === 'Incomes'">
      <h2>Incomes</h2>
      <button @click="showForm = !showForm" class="add-income-button">+ Add new Income</button>
      <IncomesForm v-if="showForm" @submitForm="handleIncomeSubmission" />
    </div>
  
  <div v-if="selectedContent === 'Expenses'">
    <button @click="showForm = !showForm">Add new Expense</button>
    <div v-if="showForm">
      <form @submit.prevent="submitExpense">
        <input type="number" v-model="expense.amount" placeholder="Amount" required />
        <input type="text" v-model="expense.category" placeholder="Category" required />
        <input type="date" v-model="expense.date" placeholder="Date" required />
        <button type="submit">Submit Expense</button>
      </form>
    </div>
    </div>
</div>
</template>

<script>
import IncomesForm from '@/components/incomes-forms.vue';

export default {
  name: "HomeForm",
    components: {
    IncomesForm
  },
   props: {
    selectedContent: {
      type: String,
      default: 'Incomes' // We set the Incomes as the default selection
    }
   },
   data() {
    return {
      showForm: false,
      income: { amount: '', description: '', source: '', date: '' },
      expense: { amount: '', category: '', date: '' }
    };
  },
  methods: {
    toggleSidebar() {
      this.$emit('toggleSidebar');
    },
    submitIncome() {
      console.log("Income submitted:", this.income);
      this.resetForm();
    },
    submitExpense() {
      console.log("Expense submitted:", this.expense);
      this.resetForm();
    },
    resetForm() {
      this.showForm = false;
      this.income = { amount: '', source: '', date: '' };
      this.expense = { amount: '', category: '', date: '' };
      this.debt = { amount: '', creditor: '', date: '' };
    }
  }
};
</script>

<style scoped>
.menu-button {
    background: none;
    border: none;
    cursor: pointer;
    transition: transform 0.2s ease-in-out;
    padding: 15px;
    margin-left: -15px;
    z-index: 1000; 
}

.menu-button svg {
  fill: #21255B;
  transition: transform 0.2s ease-in-out;
}

.menu-button svg:hover {
  transform: scale(1.1);
}


.add-income-button, .add-expense-button {
  background-color: #00B8D4;
  color: white;
  border: none;
  padding: 10px 15px;
  border-radius: 5px;
  cursor: pointer;
  margin-top: 15px;
}

.add-income-button:hover, .add-expense-button:hover {
  background-color: #00A0BE;
}
</style>

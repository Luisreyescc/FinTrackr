<template>
<div class="home-form">
  <!-- First seccion: Sidebar -->
  <div class="sidebar">
  <button @click="$emit('toggleSidebar')" class="menu-button">
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 512" width="32" height="32">
      <path d="M278.6 233.4c12.5 12.5 12.5 32.8 0 45.3l-160 160c-12.5 12.5-32.8 12.5-45.3 0s-12.5-32.8 0-45.3L210.7 256 73.4 118.6c-12.5-12.5-12.5-32.8 0-45.3s32.8-12.5 45.3 0l160 160z"/>
    </svg>
  </button>
  </div>

  <!-- Second seccion: Main content -->
  <div v-if="selectedContent === 'Incomes'">
    <div class="main-content">
      <div class="first-content">
	<div class="header">
          <h2 class="section-title">{{ selectedContent }}</h2>
          <button @click="showForm = !showForm" class="add-income-button">+ Add new Income</button>
	</div>
	
	<div class="activity-content">
          <div class="activity-section">
            <h3>Activity</h3>
          </div>
	</div>
      </div>
      
      <div class="forms-section" v-if="showForm">
	<IncomesForm @submitForm="handleIncomeSubmission" />
      </div>
    </div>
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
      showForm: false
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
    },
    handleIncomeSubmission(incomeData) {
      this.$emit('submitIncome', incomeData);
      this.showForm = false;
    }
  }
};
</script>

<style scoped>
.home-form {
  display: flex;
  width: 100%;
}

.sidebar {
  width: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.menu-button {
    background: none;
    border: none;
    cursor: pointer;
    transition: transform 0.2s ease-in-out;
    padding: 15px;
    margin-top: -40px;
    margin-left: 15px;
    z-index: 1000; 
}

.menu-button svg {
  fill: #21255B;
  transition: transform 0.2s ease-in-out;
}

.menu-button svg:hover {
  transform: scale(1.1);
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 20px;
}

.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}

.section-title {
  font-size: 24px;
  font-weight: bold;
  color: #333;
}

.add-income-button {
  background-color: #00B8D4;
  color: white;
  border: none;
  padding: 10px 15px;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
  transition: background-color 0.2s;
}

.add-income-button:hover {
  background-color: #00A0BE;
}

.activity-section {
  margin-top: 20px;
}

.form-section {
  width: 300px;
  background-color: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
  margin-left: 20px;
}
</style>

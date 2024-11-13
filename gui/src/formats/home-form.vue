<template>
<div class="home-form">
  <!-- First seccion: Sidebar -->
  <div class="sidebar">
    <button @click="$emit('toggleSidebar')" class="menu-button">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512" width="32" height="32">
	<path d="M0 96C0 78.3 14.3 64 32 64l384 0c17.7 0 32 14.3 32 32s-14.3 32-32 32L32 128C14.3 128 0 113.7 0 96zM0 256c0-17.7 14.3-32 32-32l384 0c17.7 0 32 14.3 32 32s-14.3 32-32 32L32 288c-17.7 0-32-14.3-32-32zM448 416c0 17.7-14.3 32-32 32L32 448c-17.7 0-32-14.3-32-32s14.3-32 32-32l384 0c17.7 0 32 14.3 32 32z"/>
      </svg>
    </button>
  </div>
  
  <!-- Second seccion: Main content -->
  <div v-if="selectedContent === 'Incomes'">
    <div class="main-content">
      <div class="first-content">
	<div class="header">
          <h2 class="section-title">{{ selectedContent }}</h2><IncomeButton @click="toggleForm" />
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
import IncomeButton from '@/components/incomes-header.vue';

export default {
  name: "HomeForm",
    components: {
      IncomesForm,
      IncomeButton
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
    toggleForm() {
      this.showForm = !this.showForm;
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
    overflow: hidden;
    position: relative;
    font-family: "Wix Madefor Display", sans-serif;
}

.sidebar {
    width: 50px;
    display: flex;
    align-items: center;
    justify-content: center;
    padding-top: 20px;
    position: fixed;
    z-index: 1000;
    font-family: "Wix Madefor Display", sans-serif;
}

.menu-button {
    background: none;
    border: none;
    cursor: pointer;
    transition: transform 0.2s ease-in-out;
    padding: 15px;
    margin-top: -10px;
    margin-left: 25px;
}

.menu-button svg {
    fill: #21255B;
    transition: transform 0.2s ease-in-out;
}

.menu-button svg:hover {
    transform: scale(1.1);
}

.main-content {
    display: flex;
    flex: 1;
    flex-direction: row;
    padding: 20px;
    gap: 20px;
    margin-left: 70px;
}

.first-content {
    flex: 2;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
}

.header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 20px;
    font-family: "Wix Madefor Display", sans-serif;
}

.section-title {
    font-size: 24px;
    font-weight: bold;
    margin-right: 50px; 
    color: #333;
    font-family: "Wix Madefor Display", sans-serif;
}

.add-income-button {
    border: none;
    padding: 10px 15px;
    border-radius: 5px;
    margin-left: 50px; 
    cursor: pointer;
    font-weight: bold;
    transition: background-color 0.2s;
}

.add-income-button:hover {
    background-color: #00A0BE;
}

.activity-section h3 {
    font-family: "Wix Madefor Display", sans-serif;
    margin-top: 0;
    text-align: left;
}

.forms-section {
    width: 300px;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
    display: flex;
    flex-direction: column;
    height: 100%;
}
</style>

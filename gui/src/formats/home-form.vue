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
            <h3>Activity</h3><div class="income-list">
              <IncomeRow v-for="(income, index) in incomes" :key="index" :income="income" />
            </div>
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
import IncomeRow from '@/components/income-row.vue';

export default {
  name: "HomeForm",
    components: {
      IncomesForm,
      IncomeButton,
      IncomeRow
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
      incomes: []
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
    addIncome(incomeData) {
      this.incomes.push(incomeData);
      this.showForm = false;
      //This line is just for test incomes rows in frontend
      this.saveIncomesToLocalStorage();
    },
    // end of 'methods:'}
    //This methods are for frontends tests 
    handleIncomeSubmission(incomeData) {
      //this.$emit('submitIncome', incomeData);
      //this.showForm = false;
      this.addIncome(incomeData);
    },
    saveIncomesToLocalStorage() {
      // Convert incomes array to JSON and store in localStorage
      localStorage.setItem('incomes', JSON.stringify(this.incomes));
    },
    loadIncomesFromLocalStorage() {
      // Retrieve incomes data from localStorage, if it exists
      const storedIncomes = localStorage.getItem('incomes');
      if (storedIncomes) {
        // Parse the stored JSON data and assign it to incomes
        this.incomes = JSON.parse(storedIncomes);
      }
    }
  },
  mounted() {
    // Load incomes from localStorage when the component is mounted
    this.loadIncomesFromLocalStorage(); 
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

.main-content {
    display: flex;
    flex: 1;
    flex-direction: row;
    padding: 20px;
    margin-left: 70px;
    height: 90vh;
    box-sizing: border-box;
}

.first-content {
    flex: 2;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
    flex-direction: column;
    max-width: 900px;
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
    color: #333;
    font-family: "Wix Madefor Display", sans-serif;
}

.add-income-button {
    border: none;
    padding: 10px 15px;
    border-radius: 5px;
    margin-left: 300px; 
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

.activity-section {
    flex: 1;
    overflow-y: auto;
    padding-right: 10px;
    padding-bottom: 20px;
    margin-top: 10px;
    box-sizing: border-box;
}

.activity-section {
    flex: 1;
    overflow-y: auto;
    padding-right: 10px;
    margin-top: 10px;
    box-sizing: border-box;
    max-height: 680px;
    scrollbar-width: thin;
    scrollbar-color: #00A0BE #e0e0e0;
}

.activity-content {
    flex: 1; 
    display: flex;
    flex-direction: column;
    overflow: hidden;
}

.income-list {
    max-width: 100%;
    margin-top: 10px;
}

.forms-section {
    flex: 2;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
}
</style>

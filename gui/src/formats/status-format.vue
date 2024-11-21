<template>
<div class="status-form">
  <div class="content-wrapper">
    <div class="status-container">
      <div class="header">
        <h2 class="section-title">Your account status</h2>
	<FilterGraphics
	:filterOptions="['Day', 'Fortnight', 'Month', 'Year']"
        :currentFilter="currentFilter"
        @filterSelected="applyFilter" />
	</div>
	<div class="graphics-content">
	<apexchart
            v-if="chartSeriesIncomes.length > 0"
            type="bar"
            :options="chartOptionsIncomes"
            :series="chartSeriesIncomes"
            height="400" />
	</div>
      </div>
    </div>
    
    <div v-if="localSelectedContent === 'Expenses'" class="main-content">
      <div class="expenses-container">
	<div class="header">
	<h2 class="section-title">{{ selectedContent }}</h2>
	<ShowAll @click="showAll" />
	<FilterGraphics
	:filterOptions="['Categories', 'Day', 'Week', 'Month', 'Year']"
        :currentFilter="currentFilter"
        @filterSelected="applyFilter" />
	</div>
	<div class="graphics-content">
	<apexchart
            v-if="chartSeriesExpenses.length > 0"
            type="bar"
            :options="chartOptionsExpenses"
            :series="chartSeriesExpenses"
            height="400" />
	</div>
      </div>
    </div>
  </div>
</div>
</template>

<script>
import FilterGraphics from "@/components/filter-graphics.vue";
import ApexCharts from 'vue3-apexcharts';
import axios from 'axios';

export default {
  name: "StatusForm",
  components: {
    apexchart: ApexCharts,
    FilterGraphics
  },
  props: {
    selectedContent: {
      type: String,
      default: 'Incomes',
    },
  },
  data() {
    return {
      localSelectedContent: this.selectedContent,
      incomes: [],
      expenses: [],
      chartSeriesIncomes: [],
      chartSeriesExpenses: [],
      chartOptionsIncomes: {
        chart: {
          height: 350,
          type: 'bar',
        },
        xaxis: {
          categories: [],
        },
        colors: ['#1E90FF'], // Blue for incomes
      },
      chartOptionsExpenses: {
        chart: {
          height: 350,
          type: 'bar',
        },
        xaxis: {
          categories: [],
        },
        colors: ['#FF6347'], // Red for expenses
      },
      currentFilter: "Month",
    };
  },
  methods: {
    toggleSidebar() {
      this.$emit('toggleSidebar');
    },
    updateContent(content) {
      this.localSelectedContent = content;
      this.fetchData();
    },
    async fetchData() {
      try {
        const token = localStorage.getItem("token");
        if (!token) return console.error("No token found");
        const [incomeResponse, expenseResponse] = await Promise.all([
          axios.get('http://localhost:8000/api/incomes/', {
            headers: { Authorization: `Bearer ${token}` },
          }),
          axios.get('http://localhost:8000/api/expenses/', {
            headers: { Authorization: `Bearer ${token}` },
          }),
        ]);
	
        this.incomes = incomeResponse.data;
        this.expenses = expenseResponse.data;
        this.updateCharts();
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    },
    updateCharts() {
      const incomeCategories = this.incomes.map(income => income.date);
      const incomeData = this.incomes.map(income => income.amount);
      
      this.chartSeriesIncomes = [{ name: 'Incomes', data: incomeData }];
      this.chartOptionsIncomes.xaxis.categories = incomeCategories;

      const expenseCategories = this.expenses.map(expense => expense.date);
      const expenseData = this.expenses.map(expense => expense.amount);
      
      this.chartSeriesExpenses = [{ name: 'Expenses', data: expenseData }];
      this.chartOptionsExpenses.xaxis.categories = expenseCategories;
    },
    applyFilter(filter) {
      this.currentFilter = filter;
      this.fetchData(); 
    },
    mounted() {
      this.fetchData();
    },
  },
};
</script>

<style scoped>
.status-form {
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
    background: none;
    border: none;
    cursor: pointer;
    margin-top: -15px;
    margin-left: 5px;
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

.graphics-content {
    display: flex;
    flex-direction: column;
    margin-bottom: 180px;
    max-height: 100vh;
    overflow: hidden;
    padding: 20px;
    border-top: 1px solid #eee;
    position: relative;
}
</style>

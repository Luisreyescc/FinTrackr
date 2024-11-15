<template>
  <div class="status-form">
    <button @click="toggleSidebar" class="menu-button">
      <span class="gg-menu"></span>
    </button>
    <div class="chart-container">
      <apexchart type="pie" :options="incomeChartOptions" :series="incomeSeries"></apexchart>
      <apexchart type="pie" :options="expenseChartOptions" :series="expenseSeries"></apexchart>
    </div>
  </div>
</template>

<script>
import VueApexCharts from 'vue3-apexcharts';
import axios from 'axios';
import '@/css/menu.css';

export default {
  name: "StatusForm",
  components: {
    apexchart: VueApexCharts,
  },
  data() {
    return {
      // Chart options for income data
      incomeChartOptions: {
        chart: {
          type: 'pie',
          width: '300px',
          height: '300px',
        },
        labels: [],  // Will hold income sources
      },
      incomeSeries: [],  // Will hold total amounts for each income source

      // Chart options for expense data
      expenseChartOptions: {
        chart: {
          type: 'pie',
          width: '300px',
          height: '300px',
        },
        labels: [],  // Will hold expense categories
      },
      expenseSeries: [],  // Will hold total amounts for each expense category
    };
  },
  methods: {
    toggleSidebar() {
      this.$emit('toggleSidebar');
    },

    async fetchIncomeChartData() {
      try {
        const token = localStorage.getItem("token");
        const response = await axios.get("http://localhost:8000/api/incomes/source-summary/", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        
        // Populate income chart data
        this.incomeChartOptions.labels = response.data.map(item => item.source); // Set labels to sources
        this.incomeSeries = response.data.map(item => item.total_amount); // Set series to total amounts
      } catch (error) {
        console.error("Error fetching income chart data:", error);
      }
    },

    async fetchExpenseChartData() {
      try {
        const token = localStorage.getItem("token");
        const response = await axios.get("http://localhost:8000/api/expenses/category-summary/", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        // Populate expense chart data
        this.expenseChartOptions.labels = response.data.map(item => item.category); // Set labels to categories
        this.expenseSeries = response.data.map(item => item.total_amount); // Set series to total amounts
      } catch (error) {
        console.error("Error fetching expense chart data:", error);
      }
    },
  },
  mounted() {
    this.fetchIncomeChartData();  // Fetch income data when component mounts
    this.fetchExpenseChartData(); // Fetch expense data when component mounts
  },
};
</script>

<style scoped>
.menu-button {
  background: none;
  border: none;
  cursor: pointer;
  color: #21255B;
  transition: transform 0.2s ease-in-out;
  z-index: 1000;
  padding: 20px;
}

.chart-container {
  display: flex;
  gap: 20px; /* Adds space between the two charts */
}

.chart-container apexchart {
  width: 300px;
  height: 300px;
}
</style>

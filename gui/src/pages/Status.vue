<template>
  <div class="page-container">
    <StatusForm @toggleSidebar="toggleSidebar" />
    <div class="content">
      <div v-if="selectedContent">
        <h2>{{ selectedContent }} Status</h2>
        <div class="chart-controls">
          <button @click="toggleChart('incomes')">Toggle Incomes</button>
          <button @click="toggleChart('expenses')">Toggle Expenses</button>
        </div>
        <apexchart
          v-if="chartVisible"
          type="bar"
          :options="chartOptions"
          :series="chartSeries"
        />
      </div>
    </div>
    <SideBar :isVisible="isSidebarVisible" @closeSidebar="toggleSidebar" @selectContent="updateContent" />
  </div>
</template>

<script>
import StatusForm from '@/formats/status-format.vue';
import SideBar from '@/components/side-bar.vue';
import ApexCharts from 'vue3-apexcharts';
import axios from 'axios';

export default {
  name: 'StatusPage',
  components: {
    StatusForm,
    SideBar,
    apexchart: ApexCharts,
  },
  data() {
    return {
      isSidebarVisible: false,
      selectedContent: 'Incomes',
      incomes: [],
      expenses: [],
      chartVisible: true,
      chartSeries: [],
      chartOptions: {
        chart: {
          height: 350,
          type: 'bar',
        },
        xaxis: {
          categories: [],
        },
        colors: ['#1E90FF', '#FF6347'], // Blue for incomes, red for expenses
      },
      showIncomes: true,
      showExpenses: true,
    };
  },
  methods: {
    toggleSidebar() {
      this.isSidebarVisible = !this.isSidebarVisible;
    },
    updateContent(content) {
      this.selectedContent = content;
      this.fetchData();
    },
    async fetchData() {
      try {
        const token = localStorage.getItem("token");
        if (!token) return console.error("No token found");
        
        const incomeResponse = await axios.get('http://localhost:8000/api/incomes/', {
          headers: { Authorization: `Bearer ${token}` },
        });
        const expenseResponse = await axios.get('http://localhost:8000/api/expenses/', {
          headers: { Authorization: `Bearer ${token}` },
        });
        this.incomes = incomeResponse.data;
        this.expenses = expenseResponse.data;
        this.updateChart();
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    },
    toggleChart(type) {
      if (type === 'incomes') this.showIncomes = !this.showIncomes;
      if (type === 'expenses') this.showExpenses = !this.showExpenses;
      this.updateChart();
    },
    updateChart() {
      const categories = new Set();
      const incomeData = [];
      const expenseData = [];

      // Prepare income data
      if (this.showIncomes) {
        this.incomes.forEach(income => {
          categories.add(income.date);
          incomeData.push({ x: income.date, y: income.amount });
        });
      }

      // Prepare expense data
      if (this.showExpenses) {
        this.expenses.forEach(expense => {
          categories.add(expense.date);
          expenseData.push({ x: expense.date, y: expense.amount });
        });
      }

      // Update chart
      this.chartSeries = [
        { name: 'Incomes', data: incomeData },
        { name: 'Expenses', data: expenseData },
      ];
      this.chartOptions.xaxis.categories = Array.from(categories).sort();
    },
  },
  mounted() {
    if (this.selectedContent) {
      this.fetchData();
    }
  },
};
</script>

<style scoped>
.page-container {
    display: flex;
    position: relative;
    padding-top: 70px;
    font-family: "Wix Madefor Display", sans-serif;
}

.content {
  flex: 1;
  padding: 20px;
}

.chart-controls {
  margin-bottom: 10px;
}

button {
  padding: 10px 15px;
  margin-right: 10px;
  cursor: pointer;
}

apexchart {
  max-width: 100%;
}
</style>

<template>
  <div class="page-container">
    
  </div>
</template>

<script>
import StatusForm from '@/formats/status-format.vue';
import ApexCharts from 'vue3-apexcharts';
import axios from 'axios';

export default {
  name: 'StatusPage',
  components: {
    StatusForm,
    SideBar,
    apexchart: ApexCharts
  },
  data() {
    return {
      isSidebarVisible: false,
      selectedContent: 'Incomes',
      isAllStatusVisible: false,
      chartData: [],
      chartOptions: {
        chart: {
          height: 400,
          type: 'line',
        },
        xaxis: {
          categories: [],
        },
        stroke: {
          curve: 'smooth',
        },
      },
    };
  },
  methods: {
    toggleAllStatus() {
      console.log("toggleAllStatus triggered");
      this.isAllStatusVisible = !this.isAllStatusVisible;
      if (this.isAllStatusVisible) {
        this.showAllGraphics();
      }
    },
    formatDate(dateStr) {
      return new Date(dateStr).toISOString().split('T')[0];
    },
    showAllGraphics() {
      const token = localStorage.getItem("token");
      if (!token) {
        console.error("No token found");
        return;
      }

      // Fetch both Incomes and Expenses for combined chart
      Promise.all([
        axios.get('http://localhost:8000/api/incomes/', {
          headers: { Authorization: `Bearer ${token}` },
        }),
        axios.get('http://localhost:8000/api/expenses/', {
          headers: { Authorization: `Bearer ${token}` },
        }),
      ])
      .then(([incomeResponse, expenseResponse]) => {
        console.log("Income Response:", incomeResponse.data);
        console.log("Expense Response:", expenseResponse.data);

        const incomeData = incomeResponse.data.map((item) => ({
          x: this.formatDate(item.date),
          y: parseFloat(item.amount),
        }));
        const expenseData = expenseResponse.data.map((item) => ({
          x: this.formatDate(item.date),
          y: parseFloat(item.amount),
        }));

        // Generate a complete list of unique dates from both data sets
        const uniqueDates = [
          ...new Set([...incomeData, ...expenseData].map(item => item.x))
        ].sort();

        // Populate data for missing dates with y: 0 to ensure continuity
        const fillMissingData = (data, dates) => {
          const dataMap = Object.fromEntries(data.map(item => [item.x, item.y]));
          return dates.map(date => ({
            x: date,
            y: dataMap[date] || 0
          }));
        };

        this.chartData = [
          { name: 'Incomes', data: fillMissingData(incomeData, uniqueDates) },
          { name: 'Expenses', data: fillMissingData(expenseData, uniqueDates) },
        ];

        // Set xaxis categories based on unique dates from both data sets
        this.chartOptions = {
          ...this.chartOptions,
          xaxis: {
            categories: uniqueDates,
          }
        };

        console.log("Chart Data:", this.chartData);
        console.log("Categories:", this.chartOptions.xaxis.categories);

        // Trigger Vue reactivity for chartOptions
        this.chartOptions = { ...this.chartOptions };
      })
      .catch((error) => console.error('Error fetching all data for the graphics:', error));
    },
    toggleSidebar() {
      this.isSidebarVisible = !this.isSidebarVisible;
    },
    updateContent(content) {
      this.selectedContent = content;
      this.isSidebarVisible = false;
    }
  }
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

.all-status-button {
  position: fixed;
  bottom: 20px;
  right: 20px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: background-color 0.3s;
}

.all-status-button:hover {
  background-color: #45a049;
}

.all-status-container {
  position: fixed;
  top: 80px;
  left: 50%;
  transform: translateX(-45%);
  width: 90%;
  max-width: 800px;
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  z-index: 1000;
  padding: 20px;
}

.all-status-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #ddd;
  padding-bottom: 10px;
}

.all-status-header h2 {
  font-size: 24px;
  font-weight: bold;
  color: #333;
}

.close-button {
  background: none;
  border: none;
  color: #333;
  font-size: 20px;
  cursor: pointer;
}

.all-status-content {
  padding-top: 20px;
}
</style>

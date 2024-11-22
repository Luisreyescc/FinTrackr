<template>
<div class="status-form">
  <div class="sidebar">
    <button @click="toggleSidebar" class="menu-button">
      <font-awesome-icon :icon="['fas', 'bars']" font-size="32"/>
    </button>
  </div>
  
  <div class="content-wrapper">
    <div class="section">
      <div class="header">
	<h2 class="section-title">Account Status</h2>
	<FilterGraphics
	:filterOptions="['Day', 'Fortnight', 'Month', 'Year']"
        :currentFilter="currentFilter"
        @filterSelected="applyFilter" />
      </div>
      <div class="graphic-container scrollbar">
	<div class="chart-wrapper">
	<apexchart
          v-if="chartData.length > 0"
          type="line"
          :options="chartOptions"
          :series="chartData"
          :style="{
            minWidth: '600px',
            minHeight: '400px',
            maxWidth: '100%',
            maxHeight: '100%',
            width: '100%',
            height: '100%'
          }" />
	</div>
      </div>
    </div>
    
    <div class="section">
      <div class="header">
	<h2 class="section-title">Categories Graphic</h2>
	<FilterGraphics
	:filterOptions="['Day', 'Fortnight', 'Month', 'Year']"
        :currentFilter="currentFilter"
        @filterSelected="applyFilter" />
      </div>
      <div class="graphic-container scrollbar">
	<div class="chart-wrapper">
	<apexchart
          v-if="chartData.length > 0"
          type="donut"
          :options="categoriesChartOptions"
          :series="categoriesChartData"
          :style="{
            minWidth: '600px',
            minHeight: '400px',
            maxWidth: '100%',
            maxHeight: '100%',
            width: '100%',
            height: '100%'
          }" />
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
 name: 'StatusForm',
  components: {
    apexchart: ApexCharts,
    FilterGraphics
  },
  data() {
    return {
      currentFilter: "Month",
      chartData: [],
      categoriesChartData: [],
      chartOptions: {
        chart: {
          height: 400,
          type: 'line',
          width: 400,
        },
        xaxis: {
          categories: [],
        },
        stroke: {
          curve: 'smooth',
        },
      },
      categoriesChartOptions: {
        chart: {
          type: 'donut',
        },
        labels: [], // Labels for the donut chart
      },
    };
  },
  created() {
    this.fetchLineChartData();
    this.fetchDonutChartData();
  },
  methods: {
    applyFilter(filter) {
      this.currentFilter = filter;
      console.log("Filter applied:", filter);
      // Future logic for filter graphic by date
    },
    formatDate(dateStr) {
      return new Date(dateStr).toISOString().split('T')[0];
    },
    fetchLineChartData() {
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
      this.$emit('toggleSidebar');
    },
    async fetchDonutChartData() {
      const token = localStorage.getItem('token');
      if (!token) {
        console.error('No token found');
        return;
      }

      try {
        const response = await axios.get('http://localhost:8000/api/expenses/category-summary/', {
          headers: { Authorization: `Bearer ${token}` }
        });

        const data = response.data; // API response
        console.log("Donut Chart Data:", data);

        const amounts = data.map(item => item.total_amount);
        const categories = data.map(item => item.category);

        this.categoriesChartData = amounts; // Populate series
        this.categoriesChartOptions = {
          ...this.categoriesChartOptions,
          labels: categories // Populate labels
        };

        console.log("Donut Chart Series:", this.categoriesChartData);
        console.log("Donut Chart Labels:", this.categoriesChartOptions.labels);
      } catch (error) {
        console.error('Error fetching donut chart data:', error);
      }
    },
  }
};
</script>

<style scoped>
.status-form {
    display: flex;
    width: 100%;
    height: 100%;
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
    position: relative;
    justify-content: center;
    gap: 5px;
    padding: 20px;
    margin-left: 50px;
    width: 100%;
    height: 100%;
    overflow: hidden;
}

.section {
    display: flex;
    flex-direction: column;
    width: 100%;
    border-radius: 8px;
    box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
    background-color: #ffffff;
    overflow: hidden;
}

.header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 10px 20px;
    border-bottom: 1px solid #ddd;
    font-family: "Wix Madefor Display", sans-serif;
}

.section-title {
    font-size: 24px;
    font-weight: bold;
    color: #25253C;
    font-family: "Wix Madefor Display", sans-serif;
}

.graphic-container {
    flex: 1;
    display: flex;
    justify-content: flex-start;
    align-items: center;
    overflow-x: auto;
    overflow-y: hidden;
    background-color: #ffffff;
    border-top: 1px solid #eee;
    border-radius: 8px;
}

.chart-wrapper {
    min-width: 600px;
    min-height: 400px;
    max-width: 100%;
    max-height: 100%;
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 20px;
}
</style>

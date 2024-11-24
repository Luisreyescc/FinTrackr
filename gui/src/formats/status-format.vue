<template>
<div class="status-form">
  <div class="sidebar">
    <button @click="toggleSidebar" class="menu-button">
      <font-awesome-icon :icon="['fas', 'bars']" font-size="32"/>
    </button>
  </div>
  
  <div class="content-wrapper">
    <div v-if="selectedContent === 'Account'" class="section">
      <div class="header">
        <h2 class="section-title">Account Status</h2>
	<div class="section-filter">
          <h3>End date:</h3>
          <input id="end-date" type="date" class="date-input" />
          <h3>Filtered by:</h3><h3>{{ currentFilter }}</h3>
          <FilterGraphics
            :filterOptions="['Day', 'Fortnight', 'Month', 'Year', Custom]"
            :currentFilter="currentFilter"
            @filterSelected="applyFilter" />
	</div>
      </div>
      <div class="main-content">
	<div class="graphic-container">
          <apexchart
            v-if="chartData.length > 0"
            type="area"
            :options="chartOptions"
            :series="chartData"
            :style="{ width: '100%', height: '300px' }" />
        </div>
	<div class="stats-container">
          <div class="stats-box">
            <div class="stats-header">
              <h3>Your network</h3>
              <font-awesome-icon :icon="['fas', 'piggy-bank']" class="icon" />
            </div>
            <p>{{ network }}</p>
          </div>
          <div class="stats-box">
            <div class="stats-header">
              <h3>Your incomes</h3>
              <font-awesome-icon :icon="['fas', 'circle-dollar-to-slot']" class="icon" />
            </div>
            <p>{{ incomes }}</p>
          </div>
          <div class="stats-box">
            <div class="stats-header">
              <h3>Your expenses</h3>
              <font-awesome-icon :icon="['fas', 'money-bill-transfer']" class="icon" />
            </div>
            <p>{{ expenses }}</p>
          </div>
          <div class="stats-box">
            <div class="stats-header">
              <h3>Pending debts</h3>
              <font-awesome-icon :icon="['fas', 'hand-holding-dollar']" class="icon" />
            </div>
            <p>{{ debts }}</p>
          </div>
	</div>
      </div>
    </div>
    
    <div v-if="selectedContent === 'Categories'" class="section">
      <div class="header">
	<h2 class="section-title">Categories Graphic</h2>
	<FilterGraphics
          :filterOptions="['Day', 'Fortnight', 'Month', 'Year']"
          :currentFilter="currentFilter"
          @filterSelected="applyFilter" />
      </div>
      <div class="graphic-container">
	<div class="chart-wrapper">
          <apexchart
            v-if="chartData.length > 0"
            type="donut"
            :options="categoriesChartOptions"
            :series="categoriesChartData"
            :style="{
            minWidth: '880px',
            maxWidth: '880px',
            minHeight: '880px',
            maxHeight: '880px',
            width: '880px',
            height: '880px'
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
import '@/css/scrollbar.css';
import axios from 'axios';

export default {
 name: 'StatusForm',
  components: {
    apexchart: ApexCharts,
    FilterGraphics
  },
  props: {
    selectedContent: {
      type: String,
      default: 'Account',
    },
  },
  data() {
    return {
      currentFilter: "Month",
      chartData: [],
      categoriesChartData: [],
      chartOptions: Object.freeze({
        chart: {
          type: 'area'
        },
        xaxis: {
          categories: [],
        },
	dataLabels: {
          enabled: false
        },
	colors: ['#008FFB', '#FAA700'],
        stroke: {
          curve: 'straight',
        },
      }),
      categoriesChartOptions: Object.freeze({
        chart: {
          type: 'donut'
        },
        labels: [], // Labels for the donut chart
      }),
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
  },
  mounted() {
    this.fetchLineChartData();
    if (this.selectedContent === "Account") {
      this.fetchLineChartData();
    } else if (this.selectedContent === "Categories") {
      this.fetchDonutChartData();
    }
  },
  watch: {
    selectedContent(newValue) {
      if (newValue === "Account") {
        this.fetchLineChartData();
      } else if (newValue === "Categories") {
        this.fetchDonutChartData();
      }
    }
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
    padding: 20px;
    margin-left: 50px;
}

.section {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 10px 20px;
    border-radius: 8px;
    background-color: #ffffff;
    border-bottom: 1px solid #ddd;
    box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
}

.section-title {
    font-size: 32px;
    font-weight: bold;
    color: #25253C;
    font-family: "Wix Madefor Display", sans-serif;
}

.section-filter {
    display: flex;
    align-items: center;
    gap: 15px;
    font-size: 18px;
}

.date-input,
select {
    padding: 5px;
    border-radius: 5px;
    border: 1px solid #ddd;
    font-family: "Wix Madefor Display", sans-serif;
}

.main-content {
    display: flex;
    gap: 20px;
    justify-content: space-between;
}

.graphic-container {
    flex: 1;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
    background-color: #ffffff;
    height: 300px;
}

.stats-content {
    display: grid;
    gap: 30px;
    padding: 20px;
    justify-content: center;

    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
}

.stats-box {
    text-align: center;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    flex: 1;
    gap: 50px;
    margin: 20px;
    padding: 40px;
    width: 400px;
    border-radius: 8px;
    box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
    background-color: #ffffff;
}

.stats-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    width: 100%;
    gap: 10px;
}

.stats-header h3 {
    font-size: 24px;
    font-weight: bold;
    color: #25253C;
    margin: 0;
}

.icon {
    font-size: 36px;
}

.stats-box p {
    font-size: 24px;
    font-weight: bold;
    margin: 0;
    color: #333;
}
</style>

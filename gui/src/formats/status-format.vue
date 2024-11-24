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
          <h3>Status date:</h3>
          <input id="end-date" type="date" class="date-input" />
          <h3>Filtered by: {{ currentFilter }}</h3>
          <FilterGraphics
            :filterOptions="['Day', 'Fortnight', 'Month', 'Year', Custom]"
            :currentFilter="currentFilter"
            @filterSelected="applyFilter" />
	</div>
      </div>
      <div class="main-content">
	<div class="graphic-container">
          <div class="chart-area">
            <apexchart
              v-if="chartData.length > 0"
              type="area"
              :options="chartOptions"
              :series="chartData"
              :style="{ width: '100%', height: '100%' }" />
          </div>
	</div>
	<div class="stats-container">
          <div class="stats-box">
            <div class="stats-header">
              <h3>Your network:</h3>
              <font-awesome-icon :icon="['fas', 'piggy-bank']" class="icon" />
            </div>
            <p v-html="currency"></p>
          </div>
          <div class="stats-box">
            <div class="stats-header">
              <h3>Your incomes this  {{ currentFilter}}:</h3>
              <font-awesome-icon :icon="['fas', 'circle-dollar-to-slot']" class="icon" />
            </div>
            <p v-html="incomes"></p>
          </div>
          <div class="stats-box">
            <div class="stats-header">
              <h3>Your expenses this  {{ currentFilter}}:</h3>
              <font-awesome-icon :icon="['fas', 'money-bill-transfer']" class="icon" />
            </div>
            <p v-html="expenses"></p>
          </div>
          <div class="stats-box">
            <div class="stats-header">
              <h3>Pending debts this  {{ currentFilter}}:</h3>
              <font-awesome-icon :icon="['fas', 'hand-holding-dollar']" class="icon" />
            </div>
            <p v-html="debts"></p>
          </div>
	</div>
      </div>
    </div>
    
    <div v-if="selectedContent === 'Categories'" class="section">
      <div class="header">
	<h2 class="section-title">Categories Graphic</h2>
	<FilterGraphics
          :filterOptions="['Day', 'Fortnight', 'Month', 'Year', 'Custom']"
          :currentFilter="currentFilter"
          @filterSelected="applyFilter" />
      </div>
      <div class="graphic-container">
	<div class="chart-pie">
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
          type: 'area',
          height: 650,
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
    applyFilter(filter) {
      this.currentFilter = filter;
      console.log("Filter applied:", filter);
      // Future logic for filter graphic by date
    },
    formatCurrency(amount, isNegative = false) {
      const formatted = new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 2,
        maximumFractionDigits: 2,
      }).format(amount);

      const [integerPart, decimalPart] = formatted.replace('$', '').split('.');
      const sign = isNegative ? '-' : '';

      return `<span><span class="integer-part">${sign}$</span>${integerPart}<sup class="decimal-part">${decimalPart}</sup></span>`;
    },
    formatCount(count) {
      if (count > 999999999999999) {
        return '999,999,999,999,999';
      }
      return count.toLocaleString();
    },
    getNetwork() {
      const networkAmount = 3456789.99; //
      const amount = this.formatCurrency(networkAmount, false);

      return `<span <span style="color: #25253C;">${amount}</span>`;
    },
    getIncomes() {
      const incomeCount = 15000; //get incomes count  on date by the filter selected
      const incomeAmount = 917075; //get incomes amount on date by the filter selected

      const count = this.formatCount(incomeCount);
      const amount = this.formatCurrency(incomeAmount);

      return `<span class="count-part">${count}:</span> <span style="color: #4CAF50;">${amount}</span>`;
    },
    getExpenses() {
      const expenseCount = 12000; //get expenses count on date by the filter selected
      const expenseAmount = 83456789.45; //get expenses amount on date by the filter selected

      const count = this.formatCount(expenseCount);
      const amount = this.formatCurrency(expenseAmount, true);

      return `<span class="count-part">${count}:</span> <span style="color: #21255b;">${amount}</span>`;
    },
    getDebts() {
      const debtCount = 5000; //get debts count on date by the filter selected
      const debtAmount = 3456789.99; //get debts amount on date by the filter selected

      const count = this.formatCount(debtCount);
      const amount = this.formatCurrency(debtAmount, true);

      return `<span class="count-part">${count}:</span> <span style="color: darkred;">${amount}</span>`;
    },
    toggleSidebar() {
      this.$emit('toggleSidebar');
    },
  },
  computed: {
    currency() {
      return this.getNetwork();
    },
    incomes() {
      return this.getIncomes();
    },
    expenses() {
      return this.getExpenses();
    },
    debts() {
      return this.getDebts();
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
    gap: 10px;
    justify-content: space-between;
}

.graphic-container {
    flex: 1;
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: 20px;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
    background-color: #ffffff;
    width: 100%;
    height: 670px;
    overflow: hidden;
}

.chart-area {
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    overflow: hidden;
}

.chart-pie {
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

.stats-content {
    display: grid;
    gap: 20px;
    padding: 20px;
    justify-content: center;
}

.stats-box {
    text-align: center;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    flex: 1;
    gap: 20px;
    margin: 20px;
    margin-right: 0px;
    padding: 20px;
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
    flex-direction: column;
    margin: 0;
}

.icon {
    font-size: 36px;
}

.stats-box p {
    display: flex;
    flex-direction: column;
    align-items: center;
    font-weight: bold;
    margin: 0;
    color: #333;
    font-size: 28px;
}

.count-part {
    font-size: 20px;
    font-weight: bold;
    color: #25253C;
}

.interger-part {
    font-size: 44px;
    vertical-align: top;
    margin-right: 4px;
}

.decimal-part {
    vertical-align: super;
}
</style>

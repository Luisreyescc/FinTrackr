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
          <input id="end-date" type="date" class="date-input" v-model="selectedDate" />
          <h3>Filtered by: {{ currentFilter }}</h3>
          <FilterGraphics
            :filterOptions="['All', 'Day', 'Fortnight', 'Month', 'Year']"
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
              :style="{ width: '100%', height: '90%' }" />
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
              <h3>Your incomes this {{ currentFilter }}:</h3>
              <font-awesome-icon :icon="['fas', 'circle-dollar-to-slot']" class="icon" />
            </div>
            <p v-html="incomes"></p>
          </div>
          <div class="stats-box">
            <div class="stats-header">
              <h3>Your expenses this {{ currentFilter }}:</h3>
              <font-awesome-icon :icon="['fas', 'money-bill-transfer']" class="icon" />
            </div>
            <p v-html="expenses"></p>
          </div>
          <div class="stats-box">
            <div class="stats-header">
              <h3>Pending debts this {{ currentFilter }}:</h3>
              <font-awesome-icon :icon="['fas', 'hand-holding-dollar']" class="icon" />
            </div>
            <p v-html="debts"></p>
          </div>
        </div>
      </div>
    </div>
      
    <div v-if="selectedContent === 'Categories'" class="section">
      <div class="header">
        <h2 class="section-title">Pie Charts</h2>
        <div class="section-filter">
          <h3>Status date:</h3>
          <input id="end-date" type="date" class="date-input" v-model="selectedDate" />
          <h3>Filtered by: {{ currentFilter }}</h3>
          <FilterGraphics
            :filterOptions="['All', 'Day', 'Fortnight', 'Month', 'Year']"
            :currentFilter="currentFilter"
            @filterSelected="applyFilter" />
        </div>
      </div>
      <div class="main-content">
        <div class="pie-container">
          <div class="chart-sources">
            <apexchart
              v-if="chartData.length > 0"
              type="donut"
              :options="sourcesChartOptions"
              :series="sourcesChartData"
              :style="{ width: '100%', height: '100%' }" />
          </div>
	</div>
        <div class="pie-container">
          <div class="chart-categories">
            <apexchart
              v-if="chartData.length > 0"
              type="donut"
              :options="categoriesChartOptions"
              :series="categoriesChartData"
              :style="{ width: '100%', height: '100%' }" />
          </div>
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
      currentFilter: "All",
      selectedDate: this.getTodayDate(),
      chartData: [],
      totalIncome: 0,
      totalExpense: 0,
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
      sourcesChartData: [],
      sourcesChartOptions: Object.freeze({
        chart: {
          type: 'donut'
        },
        labels: [], // Labels for the donut chart
      }),
      categoriesChartData: [],
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
    this.fetchSourcesChartData();
  },
  methods: {
    formatDate(dateStr) {
      return new Date(dateStr).toISOString().split('T')[0];
    },
    getTodayDate(){
      const today = new Date();
      const year = today.getFullYear();
      const month = String(today.getMonth() + 1).padStart(2, '0'); //Month with two digits
      const day = String(today.getDate()).padStart(2, '0'); // Day with two digits
      return `${year}-${month}-${day}`;
    },
    fetchLineChartData() {
      const token = localStorage.getItem("token");
      if (!token) {
        console.error("No token found");
        return;
      }

      const filter = this.currentFilter;
      const date = this.selectedDate;

      const url = `http://localhost:8000/api/incomes/filtered/?filter=${filter}&date=${date}`;

      // Fetch both Incomes and Expenses for combined chart
      Promise.all([
        axios.get(url, {
          headers: { Authorization: `Bearer ${token}` },
        }),
        axios.get(url.replace('incomes', 'expenses'), {
          headers: { Authorization: `Bearer ${token}` },
        }),
      ])
      .then(([incomeResponse, expenseResponse]) => {
        console.log("Income Response:", incomeResponse.data);
        console.log("Expense Response:", expenseResponse.data);

        const incomeData = incomeResponse.data.incomes.map((item) => ({
          x: this.formatDate(item.date),
          y: parseFloat(item.amount),
        }));
        const expenseData = expenseResponse.data.expenses.map((item) => ({
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

        // Update total incomes and expenses
        this.totalIncome = incomeResponse.data.total_income;
        this.totalExpense = expenseResponse.data.total_expense;

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

      const filter = this.currentFilter;
      const date = this.selectedDate;

      const url = `http://localhost:8000/api/expenses/filtered/?filter=${filter}&date=${date}`;

      try {
        const response = await axios.get(url, {
          headers: { Authorization: `Bearer ${token}` }
        });

        const data = response.data.categories_summary; // API response
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
    async fetchSourcesChartData() {
      const token = localStorage.getItem('token');
      if (!token) {
	console.error('No token found');
	return;
      }

      const filter = this.currentFilter;
      const date = this.selectedDate;

      const url = `http://localhost:8000/api/incomes/filtered/?filter=${filter}&date=${date}`;
      
      try {
	const response = await axios.get(url, {
          headers: { Authorization: `Bearer ${token}` }
	});
	
	const data = response.data.categories_summary; // API response
	console.log("Sources Chart Data:", data);
	
	const amounts = data.map(item => item.total_amount);
	const sources = data.map(item => item.category);
	
	this.sourcesChartData = amounts; // Populate series
	this.sourcesChartOptions = {
          ...this.sourcesChartOptions,
          labels: sources // Populate labels
	};
	
	console.log("Sources Chart Series:", this.sourcesChartData);
	console.log("Sources Chart Labels:", this.sourcesChartOptions.labels);
      } catch (error) {
	console.error('Error fetching sources chart data:', error);
      }
    },
    applyFilter(filter) {
      this.currentFilter = filter;
      console.log("Filter applied:", filter);
      this.fetchLineChartData();
      this.fetchDonutChartData();
    },
    formatCurrency(amount) {
      const formatted = new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 2,
        maximumFractionDigits: 2,
      }).format(Math.abs(amount));

      const [integerPart, decimalPart] = formatted.replace('$', '').split('.');
      const sign = amount < 0 ? '-' : '';

      return `<span><span class="integer-part">${sign}$</span>${integerPart}<sup class="decimal-part">${decimalPart}</sup></span>`;
    },
    formatCount(count) {
      if (count > 999999999999999) {
        return '999,999,999,999,999';
      }
      return count.toLocaleString();
    },
    getNetwork() {
      const networkAmount = this.totalIncome - this.totalExpense;
      const amount = this.formatCurrency(networkAmount, networkAmount < 0);

      return `<span <span style="color: #25253C;">${amount}</span>`;
    },
    getIncomes() {
      const amount = this.formatCurrency(this.totalIncome);

      return `<span style="color: #4CAF50;">${amount}</span>`;
    },
    getExpenses() {
      const amount = this.formatCurrency(this.totalExpense, true);

      return `<span style="color: #21255b;">${amount}</span>`;
    },
    getDebts() {
      // Placeholder for debts
      const amount = 0;
      return `<span style="color: darkred;">${amount}</span>`;
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
      this.fetchSourcesChartData();
    }
  },
  watch: {
    selectedContent(newValue) {
      if (newValue === "Account") {
        this.fetchLineChartData();
      } else if (newValue === "Categories") {
        this.fetchDonutChartData();
	this.fetchSourcesChartData();
      }
    },
    selectedDate() {
      this.fetchLineChartData();
      this.fetchDonutChartData();
      this.fetchSourcesChartData();
    },
    currentFilter() {
      this.fetchLineChartData();
      this.fetchDonutChartData();
      this.fetchSourcesChartData();
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

.pie-container {
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
    height: 100%;
    overflow: hidden;
}

.chart-sources,
.chart-categories {
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    overflow: hidden;
}
</style>

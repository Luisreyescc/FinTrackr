<template>
<div class="status-form">
  <div class="sidebar">
    <button @click="toggleSidebar" class="menu-button">
      <font-awesome-icon :icon="['fas', 'bars']" font-size="38"/>
    </button>
  </div>
  
  <div class="content-wrapper">
    <div v-if="selectedContent === 'Account'" class="section">
      <div class="header">
        <h2 class="section-title">Account Status</h2>
        <div class="section-filter">
          <h3>Status date:</h3>
          <input id="end-date" type="date" class="date-input" v-model="selectedDate"/>
          <h3>Filtered by: {{ currentFilter }}</h3>
          <FilterDropdown
            :filterOptions="['All', 'Day', 'Fortnight', 'Month', 'Year']"
            :currentFilter="currentFilter"
            @filterSelected="applyFilter"/>
        </div>
      </div>
      <div class="main-content">
        <div class="graphic-container">
          <div class="chart-area">
            <span v-if="loadingGraphics">Loading graphic...</span>
            <apexchart
              v-if="chartData.length > 0"
              type="area"
              :options="chartOptions"
              :series="chartData"
              :style="{ width: '100%', height: '90%' }"/>
          </div>
        </div>
        <div class="stats-container">
          <div class="stats-box">
            <div class="stats-header">
              <h3>Your network:</h3>
              <font-awesome-icon :icon="['fas', 'piggy-bank']" class="icon"/>
            </div>
            <p v-html="currency"></p>
          </div>
          <div class="stats-box">
            <div class="stats-header">
              <h3>Your incomes this {{ currentFilter }}:</h3>
              <font-awesome-icon :icon="['fas', 'circle-dollar-to-slot']" class="icon"/>
            </div>
            <p v-html="incomes"></p>
          </div>
          <div class="stats-box">
            <div class="stats-header">
              <h3>Your expenses this {{ currentFilter }}:</h3>
              <font-awesome-icon :icon="['fas', 'money-bill-transfer']" class="icon"/>
            </div>
            <p v-html="expenses"></p>
          </div>
          <div class="stats-box">
            <div class="stats-header">
              <h3>Pending debts this {{ currentFilter }}:</h3>
              <font-awesome-icon :icon="['fas', 'hand-holding-dollar']" class="icon"/>
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
          <input id="end-date" type="date" class="date-input" v-model="selectedDate"/>
          <h3>Filtered by: {{ currentFilter }}</h3>
          <FilterDropdown
            :filterOptions="['All', 'Day', 'Fortnight', 'Month', 'Year']"
            :currentFilter="currentFilter"
            @filterSelected="applyFilter"/>
        </div>
      </div>
      <div class="main-content">
        <div class="pie-container">
          <div class="chart-sources">
             <span v-if="loadingGraphics">Loading graphic...</span>
            <apexchart
              v-if="sourcesChartData.length > 0"
              type="donut"
              :options="sourcesChartOptions"
              :series="sourcesChartData"
              :style="{ width: '100%', height: '100%' }"/>
          </div>
	</div>
        <div class="pie-container">
          <div class="chart-categories">
            <span v-if="loadingGraphics">Loading graphic...</span>
            <apexchart
              v-if="categoriesChartData.length > 0"
              type="donut"
              :options="categoriesChartOptions"
              :series="categoriesChartData"
              :style="{ width: '100%', height: '100%' }"/>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
</template>

<script>
import FilterDropdown from "@/components/filter-dropdown.vue";
import ApexCharts from 'vue3-apexcharts';
import '@/css/scrollbar.css';
import axios from 'axios';

export default {
  name: 'StatusForm',
  components: {
    apexchart: ApexCharts,
    FilterDropdown
  },
  props: {
    selectedContent: {
      type: String,
      default: 'Account'
    },
  },
  data() {
    return {
      loadingGraphics: false,
      currentFilter: "All",
      selectedDate: this.getTodayDate(),
      chartData: [],
      totalIncome: 0,
      totalExpense: 0,
      totalDebt: 0,
      chartOptions: Object.freeze({
        chart: {
          type: 'area',
          height: 650,
        },
	legend: {
          show: true,
          fontSize: '18px',
          fontFamily: 'Wix Madefor Display, sans-serif',
        },
        xaxis: {
          labels: {
            style: {
              fontSize: '18px',
            },
          },
          categories: [],
          padding: {
            left: 100,
            right: 100
          },
        },
        yaxis: {
          labels: {
            style: {
              fontSize: '18px',
            },
          },
        },
        tooltip: {
          theme: 'dark',
        },
        dataLabels: {
          enabled: false
        },
        colors: ['#008FFB', '#FAA700', '#fA4300'],
        stroke: {
          curve: 'straight',
        },
      }),
      sourcesChartData: [],
      sourcesChartOptions: Object.freeze({
        chart: {
          type: 'donut'
        },
        legend: {
          show: true,
          fontSize: '18px',
          fontFamily: 'Wix Madefor Display, sans-serif',
          position: 'bottom',
        },
	dataLabels: {
          enabled: true,
          style: {
            fontSize: '18px',
          },
        },
        labels: [], // Labels for the donut chart
      }),
      categoriesChartData: [],
      categoriesChartOptions: Object.freeze({
        chart: {
          type: 'donut'
        },
        legend: {
          show: true,
          fontSize: '18px',
          fontFamily: 'Wix Madefor Display, sans-serif',
          position: 'bottom',
        },
	dataLabels: {
          enabled: true,
          style: {
            fontSize: '18px',
          },
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
    async fetchLineChartData() {
      const token = localStorage.getItem("token");
      if (!token) {
        console.error("No token found");
        return;
      }

      const filter = this.currentFilter;
      const date = this.selectedDate;

      const incomeUrl = `http://localhost:8000/api/incomes/filtered/?filter=${filter}&date=${date}`;
      const expenseUrl = `http://localhost:8000/api/expenses/filtered/?filter=${filter}&date=${date}`;
      const debtUrl = `http://localhost:8000/api/debts/filtered/?filter=${filter}&date=${date}`;

      try {
        this.loadingGraphics = true;
        const [incomeResponse, expenseResponse, debtResponse] = await Promise.all([
          axios.get(incomeUrl, { headers: { Authorization: `Bearer ${token}` } }),
          axios.get(expenseUrl, { headers: { Authorization: `Bearer ${token}` } }),
          axios.get(debtUrl, { headers: { Authorization: `Bearer ${token}` } })
        ]);

        const incomeData = incomeResponse.data.incomes.map(item => ({
          x: this.formatDate(item.x),
          y: parseFloat(item.y)
        }));
        const expenseData = expenseResponse.data.expenses.map(item => ({
          x: this.formatDate(item.x),
          y: parseFloat(item.y)
        }));
        const debtData = debtResponse.data.debts.map(item => ({
          x: this.formatDate(item.x),
          y: parseFloat(item.y)
        }));

        const uniqueDates = [...new Set([...incomeData, ...expenseData, ...debtData].map(item => item.x))].sort();

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
          { name: 'Debts', data: fillMissingData(debtData, uniqueDates) },
        ];

        // Set xaxis categories based on unique dates from both data sets
        this.chartOptions = {
          ...this.chartOptions,
          xaxis: {
            categories: uniqueDates,
            padding: {
              left: 100,
              right: 100
            }
          }
        };

        // Update total incomes, expenses and debts
        this.totalIncome = incomeResponse.data.total_income;
        this.totalExpense = expenseResponse.data.total_expense;
        this.totalDebt = debtResponse.data.total_debt;

        console.log("Chart Data:", this.chartData);
        console.log("Categories:", this.chartOptions.xaxis.categories);
      } catch (error) {
        console.error('Error fetching line chart data:', error);
      } finally {
        this.loadingGraphics = false;
      }
    },
    async fetchDonutChartData() {
      const token = localStorage.getItem('token');
      if (!token) {
        console.error('No token found');
        return;
      }

      const filter = this.currentFilter;
      const date = this.selectedDate;

      const expenseUrl = `http://localhost:8000/api/expenses/filtered/?filter=${filter}&date=${date}`;

      try {
	this.loadingGraphics = true;
        const response = await axios.get(expenseUrl, {
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
      } finally {
        this.loadingGraphics = false;
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

      const incomeUrl = `http://localhost:8000/api/incomes/filtered/?filter=${filter}&date=${date}`;

      try {
	this.loadingGraphics = true;
        const response = await axios.get(incomeUrl, {
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
      } finally {
        this.loadingGraphics = false;
      }
    },
    applyFilter(filter) {
      this.currentFilter = filter;
      console.log("Filter applied:", filter);
      this.chartData = [];
      this.sourcesChartData = [];
      this.categoriesChartData = [];
      this.fetchLineChartData();
      this.fetchDonutChartData();
      this.fetchSourcesChartData();
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

      return `<span <span style="color: #BF9F00;">${amount}</span>`;
    },
    getIncomes() {
      const amount = this.formatCurrency(this.totalIncome);

      return `<span style="color: #20C171;">${amount}</span>`;
    },
    getExpenses() {
      const amount = this.formatCurrency(this.totalExpense, true);

      return `<span style="color: #D55C5C;">${amount}</span>`;
    },
    getDebts() {
      const amount = this.formatCurrency(this.totalDebt, true);

      return `<span style="color: #6092DE;">${amount}</span>`;
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
    if (this.selectedContent === "Categories") {
      this.fetchDonutChartData();
      this.fetchSourcesChartData();
    } 
    if (this.selectedContent === "Account") {
      this.fetchLineChartData();
    }
  },
  watch: {
    selectedContent(newValue) {
      this.chartData = [];
      this.sourcesChartData = [];
      this.categoriesChartData = [];

      if (newValue === "Categories") {
        this.fetchSourcesChartData();
        this.fetchDonutChartData();
      }
      if (newValue === "Account") {
        this.fetchLineChartData();
      }
    },
    selectedDate() {
      this.chartData = [];
      this.sourcesChartData = [];
      this.categoriesChartData = [];
      this.fetchLineChartData();
      this.fetchDonutChartData();
      this.fetchSourcesChartData();
    },
    currentFilter() {
      this.chartData = [];
      this.sourcesChartData = [];
      this.categoriesChartData = [];
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
    padding: 20px;
    background: none;
    border: none;
    cursor: pointer;
    margin-top: -25px;
    margin-left: 35px;
    color: white;
    transition: transform 0.2s ease-in-out;
}

.menu-button:hover {
    transform: scale(1.1);
}

.content-wrapper {
    flex: 1;
    padding: 20px;
    margin-left: 70px;
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
    border-radius: 20px;
    background-color: #25262B;
    border: 2px solid white;
    box-shadow: 0px 4px 8px rgba(255, 255, 255, 0.1);
}

.section-title {
    font-size: 32px;
    font-weight: bold;
    color: white;
    font-family: "Wix Madefor Display", sans-serif;
}

.section-filter {
    display: flex;
    align-items: center;
    gap: 15px;
    color: white;
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
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0px 4px 8px rgba(255, 255, 255, 0.1);
    border-radius: 20px;
    background-color: white;
    border: 2px solid white;
    width: 100%;
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
    min-width: 50%;
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
    box-shadow: 0px 4px 8px rgba(255, 255, 255, 0.1);
    border-radius: 20px;
    background-color: #25262B;
    border: 2px solid white;
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
    color: white;
    flex-direction: column;
    margin: 0;
}

.icon {
    font-size: 40px;
    color: white;
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
    border-radius: 20px;
    background-color: white;
    border: 2px solid white;
    box-shadow: 0px 4px 8px rgba(255, 255, 255, 0.1);
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

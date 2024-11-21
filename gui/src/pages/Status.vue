=<template>
  <div class="page-container">
    <SideBar :isVisible="isSidebarVisible" @closeSidebar="toggleSidebar" @selectContent="updateContent" />

    <div class="chart-container">
      <apexchart
        type="donut"
        :options="chartOptions"
        :series="series"
        height="400"
      />
    </div>
  </div>
</template>

<script>
import SideBar from '@/components/side-bar.vue';
import ApexCharts from 'vue3-apexcharts';
import axios from 'axios';

export default {
  name: 'PieChartPage',
  components: {
    SideBar,
    apexchart: ApexCharts
  },
  data() {
    return {
      isSidebarVisible: false,
      series: [], // Array for the amounts
      chartOptions: {
        chart: {
          type: 'donut',
        },
        labels: [], // Array for the categories
        responsive: [{
          breakpoint: 480,
          options: {
            chart: {
              width: 200
            },
            legend: {
              position: 'bottom'
            }
          }
        }]
      }
    };
  },
  created() {
    this.fetchChartData();
  },
  methods: {
    async fetchChartData() {
      try {
        const token = localStorage.getItem('token'); // Assuming you're using token-based auth
        const response = await axios.get('http://localhost:8000/api/expenses/category-summary/', {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });

        const data = response.data; // Assuming the API response is an array of objects
        console.log("API Data:", data);

        // Extract amounts and categories from the response
        const amounts = data.map(item => item.total_amount);
        const categories = data.map(item => item.category);

        this.series = amounts;
        this.chartOptions = {
          ...this.chartOptions,
          labels: categories // Set the labels dynamically
        };

      } catch (error) {
        console.error('Error fetching chart data:', error);
      }
    },
    toggleSidebar() {
      this.isSidebarVisible = !this.isSidebarVisible;
    },
    updateContent(content) {
      console.log('Content selected:', content);
      this.isSidebarVisible = false;
    }
  }
};
</script>

<style scoped>
.page-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-top: 70px;
  font-family: "Wix Madefor Display", sans-serif;
}

.chart-container {
  margin-top: 20px;
  width: 90%;
  max-width: 500px;
}

button {
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
}

button:hover {
  background-color: #45a049;
}
</style>

<template>
  <div class="page-container">
    <StatusForm :selectedContent="selectedContent" @toggleSidebar="toggleSidebar" />
    <SideBar :isVisible="isSidebarVisible" @closeSidebar="toggleSidebar" @selectContent="updateContent" />

    <button @click="toggleAllStatus" class="all-status-button">
      Show All Status
    </button>
    
    <div v-if="isAllStatusVisible" class="all-status-container">
      <div class="all-status-header">
        <h2>All Status</h2>
        <button @click="toggleAllStatus" class="close-button">
	<font-awesome-icon :icon="['fas', 'xmark']" class="close-button"/>
	</button>
      </div>
      <div class="all-status-content">
        <apexchart
          v-if="chartData.length > 0"
          type="line"
          :options="chartOptions"
          :series="chartData"
          height="400"
        />
      </div>
    </div>
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
      this.isAllStatusVisible = !this.isAllStatusVisible;
      if (this.isAllStatusVisible) {
        this.showAllGraphics();
      }
    },
    showAllGraphics() {
      // Fetch both Incomes and Expenses for combined chart
      Promise.all([
        axios.get('http://localhost:8000/api/incomes/', {
          headers: { Authorization: 'Bearer ${token}' },
        }),
        axios.get('http://localhost:8000/api/expenses/', {
          headers: { Authorization: 'Bearer ${token}'},
        }),
      ])
        .then(([incomeResponse, expenseResponse]) => {
          const incomeData = incomeResponse.data.map((item) => ({
            x: item.date,
            y: item.amount,
          }));
          const expenseData = expenseResponse.data.map((item) => ({
            x: item.date,
            y: item.amount,
          }));
	this.chartData = [
            { name: 'Incomes', data: incomeData },
            { name: 'Expenses', data: expenseData },
          ];
          this.chartOptions.xaxis.categories = [
            ...new Set(
              incomeResponse.data
                .concat(expenseResponse.data)
                .map((item) => item.date)
            ),
          ].sort();
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

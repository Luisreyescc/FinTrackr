<template>
<div class="page-container">
  <StatusForm @toggleSidebar="toggleSidebar" />
  <div class="content">
    <div class="view-toggle">
      <button @click="changeViewMode('Month')">Month</button>
      <button @click="changeViewMode('Year')">Year</button>
    </div>
    <apexchart type="bar" :options="chartOptions" :series="series"></apexchart>
    <button v-if="selectedContent" class="content-button">{{ selectedContent }} Status Button</button>
  </div>
  <SideBar :isVisible="isSidebarVisible" @closeSidebar="toggleSidebar" @selectContent="updateContent" />
</div>
</template>

<script>
import StatusForm from '@/formats/status-form.vue';
import SideBar from '@/components/side-bar.vue';
import VueApexCharts from "vue-apexcharts";

export default {
  name: 'StatusPage',
  components: {
    StatusForm,
    SideBar,
    apexchart: VueApexCharts
  },
  data() {
    return {
      isSidebarVisible: false,
      selectedContent: null,
      viewMode: "Month",
      series: [
        {
          name: "Ingresos",
          data: [500, 700, 800, 600, 1200, 900]
        },
        {
          name: "Egresos",
          data: [300, 400, 500, 200, 700, 600]
        }
      ],
      chartOptions: {
        chart: {
          type: "bar",
          height: 350
        },
        plotOptions: {
          bar: {
            horizontal: false,
            columnWidth: "55%",
            endingShape: "rounded"
          }
        },
        dataLabels: {
          enabled: false
        },
        stroke: {
          show: true,
          width: 2,
          colors: ["transparent"]
        },
        xaxis: {
          categories: ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio"]
        },
        yaxis: {
          title: {
            text: "$ (USD)"
          }
        },
        fill: {
          opacity: 1
        },
        tooltip: {
          y: {
            formatter: (val) => `$ ${val}`
          }
        }
      }
    };
  },
  methods: {
    toggleSidebar() {
      this.isSidebarVisible = !this.isSidebarVisible;
    },
    updateContent(content) {
      this.selectedContent = content;
      this.isSidebarVisible = false;
    },
    changeViewMode(mode) {
      this.viewMode = mode;

      if(mode == "Month"){
        this.series = [
          { name: "Ingresos", data: [500, 700, 800, 600, 1200, 900] },
          { name: "Egresos", data: [300, 400, 500, 200, 700, 600] }
        ];
        this.chartOptions.xaxis.categories = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio"]
      } else if (mode == "Year"){
        this.series = [
          { name: "Ingresos", data: [7000, 8500, 9200, 10200, 11000, 9500] },
          { name: "Egresos", data: [4000, 4800, 5600, 5100, 6300, 5800] }
        ];
        this.chartOptions.xaxis.categories = ["2018", "2019", "2020", "2021", "2022", "2023"];
      }
    }
  }
};
</script>

<style scoped>
.page-container {
    display: flex;
    position: relative;
    padding-top: 71px;
    font-family: "Wix Madefor Display", sans-serif;
}

.content {
  flex: 1;
  padding: 20px;
}

.content-button {
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
}

.view-toggle {
  margin-bottom: 20px;
}

.view-toggle button {
  padding: 10px 15px;
  margin-right: 10px;
  font-size: 14px;
  cursor: pointer;
}
</style>

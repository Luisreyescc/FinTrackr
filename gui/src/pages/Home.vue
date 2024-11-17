<template>
<div class="page-container">
  <HomeForm :selectedContent="selectedContent" @toggleSidebar="toggleSidebar" />
  
   <!-- Sidebar component, visible based on isSidebarVisible -->
  <SideBar :isVisible="isSidebarVisible" @closeSidebar="toggleSidebar" @selectContent="updateContent" />
</div>
</template>

<script>
import HomeForm from '@/formats/home-format.vue';
import SideBar from '@/components/side-bar.vue';
import apiClient from "@/apiClient.js";
  
export default {
  name: 'HomePage',
   components: {
    HomeForm,
    SideBar
  },
  data() {
    return {
      isSidebarVisible: false,
      selectedContent: 'Incomes' // We set the Incomes option as the default selection
    };
  },
  methods: {
    async newIncome(incomeData) {
      const { amount, source, description, date } = incomeData;
      if (amount && source && description && date) {
        try {
          const response = await apiClient.post("/api/incomes", incomeData);
          if (response.status === 201) {
            alert("New income added");
          } else {
            alert(response.data.error || "Failed adding new income");
          }
        } catch (error) {
          console.error("New income error:", error);
          if (error.response && error.response.data) {
            const errors = [];
            for (const key in error.response.data) {
              errors.push(`${key}: ${error.response.data[key]}`);
            }
            alert(errors.join("\n"));
          } else {
            alert("There was an issue while adding your new income. Please try again.");
          }
        }
      } else {
        alert("Please fill in all required fields.");
      }
    },
    async newExpense(expenseData) {
      const { amount, description, categories, date } = expenseData;
      if (amount && description && categories && date) {
        try {
          const response = await apiClient.post("/api/expenses", expenseData);
          if (response.status === 201) {
            alert("New expense added");
          } else {
            alert(response.data.error || "Failed adding new expense");
          }
        } catch (error) {
          console.error("New expense error:", error);
          if (error.response && error.response.data) {
            const errors = [];
            for (const key in error.response.data) {
              errors.push(`${key}: ${error.response.data[key]}`);
            }
            alert(errors.join("\n"));
          } else {
            alert("There was an issue while adding your new expense. Please try again.");
          }
        }
      } else {
        alert("Please fill in all required fields.");
      }
    },
    toggleSidebar() {
      this.isSidebarVisible = !this.isSidebarVisible;
    },
    updateContent(content) {
      this.selectedContent = content;
      this.isSidebarVisible = false; // Close sidebar after selection
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
</style>

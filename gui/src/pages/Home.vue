<template>
<div class="page-container">
  <HomeForm :selectedContent="selectedContent" @toggleSidebar="toggleSidebar" />
  <SideBar :isVisible="isSidebarVisible" @closeSidebar="toggleSidebar" @selectContent="updateContent" />
</div>

<div class="message-container">
  <MessageAlerts
    v-for="(msg, index) in messages" 
    :key="msg.id" 
    :text="msg.text" 
    :type="msg.type" 
    @close="removeMessage(index)" />
</div>
</template>

<script>
import MessageAlerts from '@/components/messages.vue';
import HomeForm from '@/formats/home-format.vue';
import SideBar from '@/components/side-bar.vue';
import apiClient from "@/apiClient.js";
  
export default {
  name: 'HomePage',
  components: {
    HomeForm,
    SideBar,
    MessageAlerts
  },
  data() {
    return {
      isSidebarVisible: false,
      selectedContent: 'Incomes', // We set the Incomes option as the default selection
      messages: []
    };
  },
  methods: {
    addMessage(text, type = "neutral") {
      const id = Date.now();
      this.messages.push({ id, text, type });
    },
    removeMessage(index) {
      this.messages.splice(index, 1);
    },
    async newIncome(incomeData) {
      const { amount, source, description, date } = incomeData;
      if (amount && source && description && date) {
        try {
          const response = await apiClient.post("/api/incomes", incomeData);
          if (response.status === 201) {
            this.addMessage("New income added succesfully.", "success");
          } else {
            this.addMessage("Failed adding the income.", "error");
          }
        } catch (error) {
          console.error("New income error:", error);
          if (error.response && error.response.data) {
            const errors = [];
            for (const key in error.response.data) {
              errors.push(`${key}: ${error.response.data[key]}`);
            }
            this.addMessage(errors.join("\n"), "error");
          } else {
            this.addMessage("There was an issue while adding your income. Please try again.", "error");
          }
        }
      }
    },
    async newExpense(expenseData) {
      const { amount, description, categories, date } = expenseData;
      if (amount && description && categories && date) {
        try {
          const response = await apiClient.post("/api/expenses", expenseData);
          if (response.status === 201) {
            this.addMessage("New expense added succesfully.", "success");
          } else {
            this.addMessage("Failed adding the expense.", "error");
          }
        } catch (error) {
          console.error("New expense error:", error);
          if (error.response && error.response.data) {
            const errors = [];
            for (const key in error.response.data) {
              errors.push(`${key}: ${error.response.data[key]}`);
            }
            this.addMessage(errors.join("\n"), "error");
          } else {
            this.addMessage("There was an issue while adding your expense. Please try again.", "error");
          }
        }
      }
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
</style>

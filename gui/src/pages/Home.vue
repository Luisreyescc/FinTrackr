<template>
<div class="page-container">
  <HomeForm :selectedContent="selectedContent" @toggleSidebar="toggleSidebar" />
  
   <!-- Sidebar component, visible based on isSidebarVisible -->
  <SideBar :isVisible="isSidebarVisible" @closeSidebar="toggleSidebar" @selectContent="updateContent" />
</div>
</template>

<script>
import HomeForm from '@/formats/home-form.vue';
import SideBar from '@/components/side-bar.vue';
  
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

.content-button {
    padding: 10px 20px;
    font-size: 16px;
    cursor: pointer;
}
</style>

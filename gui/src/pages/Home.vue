<template>
<div class="page-container">
  <HomeForm @toggleSidebar="toggleSidebar" />
  
  <!-- Conditionally render the content based on selectedContent -->
  <div class="content">
    <button v-if="selectedContent" class="content-button">{{ selectedContent }} Home Button</button>
  </div>

   <!-- Sidebar component, visible based on isSidebarVisible -->
  <SideBar
    :isVisible="isSidebarVisible"
    @closeSidebar="toggleSidebar"
    @selectContent="updateContent" />
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
      selectedContent: null
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
</style>

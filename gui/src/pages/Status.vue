<template>
  <div class="page-container">
    <StatusForm :selectedContent="selectedContent" @toggleSidebar="toggleSidebar" />
    <SideBar :isVisible="isSidebarVisible" @closeSidebar="toggleSidebar" @selectContent="updateContent" />
  </div>
</template>

<script>
import StatusForm from '@/formats/status-format.vue';
import SideBar from '@/components/side-bar.vue';
//import axios from 'axios';

export default {
  name: 'StatusPage',
  components: {
    StatusForm,
    SideBar
  },
  data() {
    return {
      isSidebarVisible: false,
      selectedContent: 'Incomes'
    };
  },
  methods: {
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

<template>
<div class="page-container scrollbar">
  <StatusForm :selectedContent="selectedContent" @toggleSidebar="toggleSidebar"/>
  <SideBar
    :isVisible="isSidebarVisible"
    :currentPage="'Status'"
    @closeSidebar="toggleSidebar"
    @selectContent="updateContent"/>
</div>
</template>

<script>
import StatusForm from '@/formats/status-format.vue';
import SideBar from '@/components/side-bar.vue';
import '@/css/scrollbar.css';

export default {
  name: 'StatusPage',
  components: {
    SideBar,
    StatusForm
  },
  data() {
    return {
      isSidebarVisible: false,
      selectedContent: 'Account',
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
    justify-content: space-between;
    padding-top: 100px;
    min-height: 100vh;
    background: #25262B;
    font-family: "Wix Madefor Display", sans-serif;
}

.content {
    flex: 1;
    padding: 20px;
    overflow: hidden;
}
</style>

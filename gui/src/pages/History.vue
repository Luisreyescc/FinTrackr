<template>
<div class="page-container scrollbar">
  <HistoryForm :selectedContent="selectedContent" @toggleSidebar="toggleSidebar"/>
  <SideBar
    :isVisible="isSidebarVisible"
    :currentPage="'History'"
    @closeSidebar="toggleSidebar"
    @selectContent="updateContent"/>
</div>
</template>

<script>
import HistoryForm from '@/formats/history-format.vue';
import SideBar from '@/components/side-bar.vue';
import '@/css/scrollbar.css';

export default {
  name: "HistoryPage",
  components: {
    SideBar,
    HistoryForm
  },
  data() {
    return {
      isSidebarVisible: false,
      selectedContent: 'History',
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

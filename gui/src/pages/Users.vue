<template>
<div class="page-container scrollbar">
  <UsersForm :selectedContent="selectedContent" @toggleSidebar="toggleSidebar"/>
  <SideBar
    :isVisible="isSidebarVisible"
    :currentPage="'UsersManagment'"
    @closeSidebar="toggleSidebar"
    @selectContent="updateContent"/>
</div>
</template>

<script>
import UsersForm from '@/formats/users-format.vue';
import SideBar from '@/components/side-bar.vue';
import '@/css/scrollbar.css';

export default {
  name: "UsersManagment",
  components: {
    SideBar,
    UsersForm
  },
  data() {
    return {
      isSidebarVisible: false,
      selectedContent: 'UsersManagment',
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
.users-page {
  padding: 20px;
}

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

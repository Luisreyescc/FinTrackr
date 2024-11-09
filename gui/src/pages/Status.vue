<template>
<div class="page-container">
  <StatusForm @toggleSidebar="toggleSidebar" />
  <div class="content">
    <button v-if="selectedContent" class="content-button">{{ selectedContent }} Status Button</button>
  </div>
  <SideBar
    :isVisible="isSidebarVisible"
    @closeSidebar="toggleSidebar"
    @selectContent="updateContent" />
</div>
</template>

<script>
import StatusForm from '@/formats/status-form.vue';
import SideBar from '@/components/side-bar.vue';
export default {
  name: 'StatusPage',
     components: {
    StatusForm,
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
      this.isSidebarVisible = false;
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

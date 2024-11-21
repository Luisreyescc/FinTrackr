<template>
<div class="page-container scrollbar">
  <StatusForm @toggleSidebar="toggleSidebar"/>
  <SideBar :isVisible="isSidebarVisible" @closeSidebar="toggleSidebar" @selectContent="updateContent" />
</div>
</template>

<script>
import StatusForm from '@/formats/status-format.vue';
import SideBar from '@/components/side-bar.vue';

export default {
  name: 'StatusPage',
  components: {
    SideBar,
    StatusForm
  },
  data() {
    return {
      isSidebarVisible: false,
    };
  },
  methods: {
    toggleSidebar() {
      this.isSidebarVisible = !this.isSidebarVisible;
    }
  }
};
</script>

<style scoped>
.page-container {
    display: flex;
    position: relative;
    justify-content: space-between;
    padding-top: 70px;
    overflow: hidden;
    font-family: "Wix Madefor Display", sans-serif;
}

.content {
    flex: 1;
    padding: 20px;
    overflow: hidden;
}
</style>

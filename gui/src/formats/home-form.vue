<template>
  <div class="home-form">
    <!-- Button to toggle the sidebar -->
    <button @click="$emit('toggleSidebar')" class="menu-button">
      <span class="gg-menu"></span>
    </button>
  </div>
</template>

<script>
import '@/css/menu.css';

export default {
  name: "HomeForm",
    methods: {
    toggleSidebar() {
      this.$emit('toggleSidebar');
    },
  },
};
</script>

<style scoped>
.menu-button {
    background: none;
    border: none;
    cursor: pointer;
    color: #21255B;
    transition: transform 0.2s ease-in-out;
    z-index: 1000;
    padding: 20px;
}
</style>

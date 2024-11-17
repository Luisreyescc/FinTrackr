<template>
  <div class="status-form">
    <button @click="$emit('toggleSidebar')" class="menu-button">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512" width="32" height="32">
	<path d="M0 96C0 78.3 14.3 64 32 64l384 0c17.7 0 32 14.3 32 32s-14.3 32-32 32L32 128C14.3 128 0 113.7 0 96zM0 256c0-17.7 14.3-32 32-32l384 0c17.7 0 32 14.3 32 32s-14.3 32-32 32L32 288c-17.7 0-32-14.3-32-32zM448 416c0 17.7-14.3 32-32 32L32 448c-17.7 0-32-14.3-32-32s14.3-32 32-32l384 0c17.7 0 32 14.3 32 32z"/>
      </svg>
    </button>
  </div>
</template>

<script>

export default {
  name: "StatusForm",
    methods: {
    toggleSidebar() {
      this.$emit('toggleSidebar');
    },
  },
};
</script>

<style scoped>
  .status-form {
    display: flex;
    width: 100%;
    overflow: hidden;
    font-family: "Wix Madefor Display", sans-serif;
  }
  
.menu-button {
    background: none;
    border: none;
    cursor: pointer;
    transition: transform 0.2s ease-in-out;
    margin-top: -283px;
    margin-left: 6px;
}

.menu-button svg {
    fill: #21255B;
    transition: transform 0.2s ease-in-out;
}

.menu-button svg:hover {
    transform: scale(1.1);
}
</style>

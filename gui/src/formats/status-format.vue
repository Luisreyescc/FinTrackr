<template>
  <div class="status-form">
    <button @click="$emit('toggleSidebar')" class="menu-button">
      <font-awesome-icon :icon="['fas', 'bars']" font-size="32"/>
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
    margin-top: -287px;
    margin-left: 8px;
    color: #25253C;
    transition: transform 0.2s ease-in-out;
}

.menu-button:hover {
    transform: scale(1.1);
}
</style>

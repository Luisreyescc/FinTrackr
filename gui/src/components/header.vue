<template>
  <header class="header">
    <div class="header-content">
      <img src="@/assets/title.png" alt="FinTrackr Logo" class="logo" />
    </div>
  </header>
</template>

<script>
export default {
  name: 'AppHeader'
};
</script>

<style scoped>
.header {
  background-color: #5860D0;
  padding: 15px 15px;
  color: #FFFFFF;
  width: 100%;
  position: fixed; /* Make it stick to the top of the page */
  top: 0;
  left: 0;
  z-index: 1000; /* Ensure it stays on top of other elements */
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  height: 40px;
  width: auto;
}
</style>

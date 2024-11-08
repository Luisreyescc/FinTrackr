<template>
  <div class="page-container">
    <div class="illustration">
      <img
        src="@/assets/empty_status.svg"
        alt="Nothing to see here"
        class="cactus-image"
      />
      <h2 class="headline">Nothing to see here</h2>
    </div>
    <div class="maintenance-message">
      <p>Status page is on maintenance...</p>
      <img src="@/assets/tools.png" alt="Maintenance" class="tools-image" />
    </div>
  </div>
</template>

<script>
export default {
  name: "StatusPage",
};
</script>

<style scoped>
.page-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: calc(100vh - 60px);
  text-align: center;
  color: #666;
  font-family: "Wix Madefor Display", sans-serif;
}

.illustration {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.cactus-image {
  width: 300px;
  height: auto;
}

.headline {
  font-size: 24px;
  font-weight: bold;
  color: #666;
}

.maintenance-message {
  display: flex;
  align-items: center;
  font-size: 18px;
  color: #333;
  margin-top: 20px;
}

.maintenance-message p {
  margin-right: 10px;
}

.tools-image {
  width: 36px;
  height: 36px;
}
</style>

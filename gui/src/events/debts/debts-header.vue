<template>
<button @click="$emit('toggle-form')" class="add-debt-button">
  <div class="icon-container">
    <font-awesome-icon :icon="['fas', 'plus']" font-size="18"/></div>
  <span class="button-text">ADD NEW DEBT</span>
</button>
</template>

<script>
export default {
  name: "DebtButton",
};
</script>

<style scoped>
.add-debt-button {
    display: flex;
    align-items: center;
    background-color: #8700D5;
    color: white;
    border: none;
    border-radius: 20px;
    overflow: hidden;
    cursor: pointer;
    font-weight: bold;
    transition: background-color 0.2s;
    font-family: "Wix Madefor Display", sans-serif;
    padding: 0;
    height: 40px;
}

.icon-container {
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: #333;
    padding: 0 10px;
    border-top-left-radius: 20px;
    border-bottom-left-radius: 20px;
    height: 100%;
}

.button-text {
    padding: 0 15px;
    background-color: #8700D5;
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100%;
}

.add-debt-button:hover .button-text {
    background-color: #A945E2;
}
</style>

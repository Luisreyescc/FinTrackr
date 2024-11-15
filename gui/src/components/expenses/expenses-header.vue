<template>
<button @click="$emit('toggle-form')" class="add-expense-button">
  <div class="icon-container">
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="16" height="16" fill="white">
      <path d="M12 2a1 1 0 0 1 1 1v8h8a1 1 0 1 1 0 2h-8v8a1 1 0 1 1-2 0v-8H3a1 1 0 1 1 0-2h8V3a1 1 0 0 1 1-1z" />
    </svg> </div>
    <span class="button-text">ADD NEW EXPENSE</span>
  </button>
</template>

<script>
export default {
  name: "ExpenseButton",
};
</script>

<style scoped>
.add-expense-button {
    display: flex;
    align-items: center;
    background-color: #FF7043;
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
    background-color: #FF7043;
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100%;
}

.add-expense-button:hover .button-text {
    background-color: #FF5722;
}
</style>

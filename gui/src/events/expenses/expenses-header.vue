<template>
<button @click="$emit('toggle-form')" class="add-expense-button">
    <span class="button-icon"><font-awesome-icon :icon="['fas', 'plus']"/></span>
  <span class="button-text">New Expense</span>
</button>
</template>

<script>
export default {
  name: "ExpenseButton"
};
</script>

<style scoped>
.add-expense-button {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 10px 20px;
    background-color: white;
    color: #25262B;
    border: 3px solid #25262B;
    border-radius: 10px;
    cursor: pointer;
    font-weight: bold;
    font-size: 16px;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    font-family: "Wix Madefor Display", sans-serif;
}

.button-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    margin-right: 15px;
    font-size: 18px;
    color: #25262B;
}

.button-text {
    font-size: 14px;
    color: #25262B;
    font-family: "Wix Madefor Display", sans-serif;
}
</style>

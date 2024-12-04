<template>
<button @click="$emit('toggle-form')" class="add-expense-button">
    <span class="button-icon"><font-awesome-icon :icon="['fas', 'plus']"/></span>
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
    width: 50px;
    height: 50px;
    border-radius: 50px;
    background-color: #25262B;
    border: 1px solid #25262B;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    cursor: pointer;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.button-icon {
    font-size: 24px;
    color: white;
}

.add-expense-button:hover {
    box-shadow: 0 6px 10px rgba(0, 0, 0, 0.15);
    transform: scale(1.1);
}
</style>

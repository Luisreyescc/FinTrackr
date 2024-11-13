<template>
  <button @click="$emit('click')" class="add-income-button">
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="16" height="16" fill="white">
      <path d="M12 2a1 1 0 0 1 1 1v8h8a1 1 0 1 1 0 2h-8v8a1 1 0 1 1-2 0v-8H3a1 1 0 1 1 0-2h8V3a1 1 0 0 1 1-1z" />
    </svg>
    <span>ADD ITEM</span>
  </button>
</template>

<script>
export default {
  name: "IncomeButton",
};
</script>

<style scoped>
.add-income-button {
  display: flex;
  align-items: center;
  background-color: #00B8D4;
  color: white;
  border: none;
  padding: 10px 15px;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
  transition: background-color 0.2s;
}

.add-income-button:hover {
  background-color: #00A0BE;
}

.add-income-button svg {
  margin-right: 8px;
}
</style>

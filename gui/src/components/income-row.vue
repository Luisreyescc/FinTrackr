<template>
  <div class="income-row">
    <div class="income-icon"></div>
    <div class="income-details">
      <h4>{{ income.source }}</h4>
      <p>{{ income.description }}</p>
      <span class="income-date">{{ income.date }}</span>
    </div>
    <div class="income-amount-section">
      <span class="income-amount">+ ${{ income.amount }}</span>
      <div class="income-actions">
        <button class="edit-button"></button>
        <button class="delete-button"></button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "IncomeRow",
  props: {
    income: {
      type: Object,
      required: true
    }
  }
};
</script>

<style scoped>
.income-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 15px;
  background-color: #F9F9F9;
  border-radius: 8px;
  margin-bottom: 10px;
  box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1);
}

.income-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: #e0e0e0;
  margin-right: 10px;
}

.income-details {
  flex: 1;
}

.income-details h4 {
  margin: 0;
  font-size: 16px;
  font-weight: bold;
}

.income-details p {
  margin: 5px 0;
  color: #777;
  font-size: 14px;
}

.income-date {
  color: #aaa;
  font-size: 12px;
}

.income-amount-section {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}

.income-amount {
  font-weight: bold;
  color: #4CAF50; /* Verde para representar ingreso */
  font-size: 16px;
}

.income-actions {
  display: flex;
  gap: 5px;
  margin-top: 5px;
}

.edit-button, .delete-button {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 16px;
}
</style>

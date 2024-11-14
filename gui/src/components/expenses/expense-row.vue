<template>
  <div class="expense-row">
    <div class="expense-icon"></div>
    <div class="expense-details">
      <h4>{{ expense.categories }}</h4>
      <p>{{ expense.description }}</p>
      <span class="expense-date">{{ expense.date }}</span>
    </div>
    <div class="expense-amount-section">
      <span class="expense-amount">{{ formattedAmount }}</span>
      <div class="expense-actions">
        <button class="edit-button"></button>
        <button class="delete-button"></button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "ExpenseRow",
  props: {
    expense: {
      type: Object,
      required: true
    }
  },
  computed: {
    formattedAmount() {
      // This for give the amount format in USD
      const formatter = new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
      });
      return `- ${formatter.format(this.expense.amount)}`;
    }
  }
};
</script>

<style scoped>
.expense-row {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  padding: 15px;
  background-color: #F9F9F9;
  border-radius: 8px;
  margin-bottom: 10px;
  box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1);
}

.expense-icon {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background-color: #e0e0e0;
  margin-right: 14px;
}

.expense-details {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    overflow: hidden;
}

.expense-details h4 {
  margin: 0;
  font-size: 16px;
  color: #21255b;
  font-weight: bold;
}

.expense-details p {
  margin: 5px 0;
  color: #777;
  font-weight: bold;
  font-size: 14px;
}

.expense-details h4, .expense-details p {
    margin: 0;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    margin-left: 10px;
}

.expense-details h4 {
  font-size: 16px;
  color: #21255b;
  font-weight: bold;
}

.expense-details p {
  color: #777;
  font-weight: bold;
  font-size: 14px;
}

.expense-date {
  color: #aaa;
  font-size: 12px;
}

.expense-amount-section {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  margin-left: 15px;
}

.expense-amount {
  font-weight: bold;
  color: #e42121;
  font-size: 16px;
  flex-shrink: 0;
}

.expense-actions {
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

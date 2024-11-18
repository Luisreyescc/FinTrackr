<template>
  <div class="expense-row">
    <div class="expense-icon">
      <font-awesome-icon :icon="['fas', 'money-bill-transfer']" font-size="28" color="black" />
    </div>
    <div class="expense-details">
      <h4>{{ formattedCategories }}</h4>
      <p class="expense-description">{{ expense.description }}</p>
      <span class="expense-date">{{ formattedDate }}</span>
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
    },
    formattedCategories() {
      return this.expense.categories.join(", ");
    },
    formattedDate() {
      // Data format day-MONTH-year
      const date = new Date(this.expense.date);
      const day = String(date.getDate()).padStart(2, '0');
      const month = date.toLocaleString('en-US', { month: 'short' }).toUpperCase();
      const year = date.getFullYear();
      return `${day}-${month}-${year}`;
    }
  }
};
</script>

<style scoped>
.expense-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 15px;
  background-color: #F9F9F9;
  border-radius: 8px;
  margin-bottom: 10px;
  box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1);
}

.expense-icon {
    display: flex;
    align-items: center;
    justify-content: center;
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

.expense-details h4, .expense-description {
    margin: 0;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 440px;
    margin-left: 10px;
}

.expense-details h4 {
  font-size: 16px;
  color: #21255b;
  font-weight: bold;
}

.expense-description {
  color: #777;
  font-weight: bold;
  font-size: 14px;
}

.expense-date {
    color: #aaa;
    font-weight: bold;
    font-size: 12px;
    margin-left: 10px;
    white-space: nowrap;
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

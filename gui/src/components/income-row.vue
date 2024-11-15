<template>
  <div class="income-row">
    <div class="income-icon"></div>
    <div class="income-details">
      <h4>{{ income.source }}</h4>
      <p class="income-description">{{ income.description }}</p>
      <span class="income-date">{{ formattedDate }}</span>
    </div>
    <div class="income-amount-section">
      <span class="income-amount">{{ formattedAmount }}</span>
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
  },
  computed: {
    formattedAmount() {
      // This for give the amount format in USD
      const formatter = new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
      });
      return `+ ${formatter.format(this.income.amount)}`;
    },
    formattedDate() {
      // Data format day-MONTH-year
      const date = new Date(this.income.date);
      const day = String(date.getDate()).padStart(2, '0');
      const month = date.toLocaleString('en-US', { month: 'short' }).toUpperCase();
      const year = date.getFullYear();
      return `${day}-${month}-${year}`;
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
    width: 60px;
    height: 60px;
    border-radius: 50%;
    background-color: #e0e0e0;
    margin-right: 14px;
}

.income-details {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    overflow: hidden;
}

.income-details h4, .income-description {
    margin: 0;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 440px;
    margin-left: 10px;
}

.income-details h4 {
    font-size: 16px;
    color: #21255b;
    font-weight: bold;
}

.income-description {
    color: #777;
    font-weight: bold;
    font-size: 14px;
}

.income-date {
    color: #aaa;
    font-weight: bold;
    font-size: 12px;
    margin-left: 10px;
    white-space: nowrap;
}

.income-amount-section {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    margin-left: 15px;
}

.income-amount {
    font-weight: bold;
    color: #4CAF50;
    font-size: 16px;
    flex-shrink: 0;
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

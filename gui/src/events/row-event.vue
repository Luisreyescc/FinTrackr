<template>
  <div :class="rowClass">
    <div class="event-icon">
      <font-awesome-icon :icon="icon" class="row-icon"/>
    </div>
    <div class="event-details">
      <h4>{{ formattedCategories }}</h4>
      <p class="event-description">{{ event.description }}</p>
      <span class="event-date">{{ formattedDate }}</span>
      <span :class="typeClass">{{ event.type }}</span>
    </div>
    <div class="event-amount-section">
      <span :class="amountClass">{{ formattedAmount }}</span>
    </div>
  </div>
</template>

<script>
export default {
  name: 'EventRow',
  props: {
    event: {
      type: Object,
      required: true
    },
  },
  computed: {
    rowClass() {
      if (this.event.type === 'Income')
        return 'income-row';
      if (this.event.type === 'Expense')
        return 'expense-row';

      return 'debt-row';
    },
    icon() {
      if (this.event.type === 'Income')
        return ['fas', 'circle-dollar-to-slot'];
      if (this.event.type === 'Expense')
        return ['fas', 'money-bill-transfer'];

      return ['fas', 'hand-holding-dollar'];
    },
    amountClass() {
      if (this.event.type === 'Income')
        return 'income-amount';
      if (this.event.type === 'Expense')
        return 'expense-amount';

      return 'debt-amount';
    },
    typeClass() {
      if (this.event.type === 'Income')
        return 'income-type';
      if (this.event.type === 'Expense')
        return 'expense-type';

      return 'debt-type';
    },
    formattedAmount() {
      const sign = this.event.type === 'Income' ? '+' : this.event.type === 'Expense' ? '-' : '';
      const formatter = new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
      });
      return `${sign}${formatter.format(this.event.amount)}`;
    },
    formattedCategories() {
      return this.event.categories ? this.event.categories.join(', ') : 'No categories';
    },
    formattedDate() {
      const date = new Date(this.event.date);
      const day = String(date.getDate()).padStart(2, '0');
      const month = date.toLocaleString('en-US', { month: 'short' }).toUpperCase();
      const year = date.getFullYear();
      return `${year}-${month}-${day}`;
    }
  },
};
</script>

<style scoped>
.income-row, .expense-row, .debt-row{
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 15px;
    background-color: #f9f9f9;
    border-radius: 8px;
    margin-bottom: 10px;
    box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1);
}

.event-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 70px;
    height: 70px;
    border-radius: 50%;
    background-color: #e0e0e0;
    margin-right: 14px;
}

.row-icon {
    font-size: 40px;
    color: #25253C;
}

.event-details {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    overflow: hidden;
}

.event-details h4, .event-description {
    margin: 0;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 440px;
    margin-left: 10px;
}

.event-details h4 {
    font-size: 22px;
    color: #25262B;
    font-weight: bold;
}

.event-description {
    color: #777;
    font-weight: bold;
    font-size: 16px;
}

.event-date {
    color: #aaa;
    font-weight: bold;
    font-size: 18px;
    margin-left: 10px;
    white-space: nowrap;
}

.event-amount-section {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    font-weight: bold;
    font-size: 20px;
    margin-left: 25px;
}

.income-amount {
    color: #4caf50;
}

.expense-amount {
    color: #f44336;
}

.debt-amount {
    color: #25262B;
}

.income-type {
    color: #4caf50;
    font-weight: bold;
    margin-top: 5px;
}

.expense-type {
    color: #f44336;
    font-weight: bold;
    margin-top: 5px;
}

.debt-type {
    color: #BF9F00;
    font-weight: bold;
    margin-top: 5px;
}
</style>

<template>
  <div :class="rowClass">
    <div class="event-icon">
      <font-awesome-icon :icon="parseIcon(event.icon)" class="row-icon"/>
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
      return this.event.categories
        ? this.event.categories.map(category => category.charAt(0).toUpperCase() + category.slice(1)).join(', ')
        : 'No categories';
    },
    formattedDate() {
      const date = new Date(this.event.date);
      const day = String(date.getDate()).padStart(2, '0');
      const month = date.toLocaleString('en-US', { month: 'short' }).toUpperCase();
      const year = date.getFullYear();
      return `${year}-${month}-${day}`;
    }
  },
  methods: {
    parseIcon(iconString) {
      if (typeof iconString === 'string') {
        return iconString.split(' ');
      }
      return iconString;
    }
  }
};
</script>

<style scoped>
.income-row, .expense-row, .debt-row{
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 15px;
    background: #25262B;
    border: 2px solid white;
    border-radius: 20px;
    margin-bottom: 10px;
    box-shadow: -2px 0 8px  rgba(255, 255, 255, 0.1);
}

.event-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 75px;
    height: 75px;
    border-radius: 50%;
    background: #25262B;
    border: 2px solid white;
    margin-right: 14px;
}

.row-icon {
    font-size: 40px;
    color: white;
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
    max-width: 420px;
    margin-left: 10px;
}

.event-details h4 {
    font-size: 22px;
    color: #D160DE;
    font-weight: bold;
}

.event-description {
    color: white;
    font-weight: bold;
    font-size: 20px;
}

.event-date {
    color: #BF9F00;
    font-weight: bold;
    font-size: 18px;
    margin-left: 10px;
    white-space: nowrap;
}

.event-amount-section {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    margin-left: 25px;
    margin-top: 5px;
}

.income-amount {
    color: #20C171;
}

.expense-amount {
    color: #D55C5C;
}

.debt-amount {
    color: #6092DE;
}

.income-type {
    color: #20C171;
    font-weight: bold;
    margin-top: 5px;
}

.expense-type {
    color: #D55C5C;
    font-weight: bold;
    margin-top: 5px;
}

.debt-type {
    color: #6092DE;
    font-weight: bold;
    margin-top: 5px;
}
</style>

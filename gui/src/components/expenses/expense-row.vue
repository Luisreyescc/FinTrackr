<template>
  <div class="expense-row">
    <div class="expense-icon">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 512" width="28" height="28" fill="black">
	<path d="M535 41c-9.4-9.4-9.4-24.6 0-33.9s24.6-9.4 33.9 0l64 64c4.5 4.5 7 10.6 7 17s-2.5 12.5-7 17l-64 64c-9.4 9.4-24.6 9.4-33.9 0s-9.4-24.6 0-33.9l23-23L384 112c-13.3 0-24-10.7-24-24s10.7-24 24-24l174.1 0L535 41zM105 377l-23 23L256 400c13.3 0 24 10.7 24 24s-10.7 24-24 24L81.9 448l23 23c9.4 9.4 9.4 24.6 0 33.9s-24.6 9.4-33.9 0L7 441c-4.5-4.5-7-10.6-7-17s2.5-12.5 7-17l64-64c9.4-9.4 24.6-9.4 33.9 0s9.4 24.6 0 33.9zM96 64l241.9 0c-3.7 7.2-5.9 15.3-5.9 24c0 28.7 23.3 52 52 52l117.4 0c-4 17 .6 35.5 13.8 48.8c20.3 20.3 53.2 20.3 73.5 0L608 169.5 608 384c0 35.3-28.7 64-64 64l-241.9 0c3.7-7.2 5.9-15.3 5.9-24c0-28.7-23.3-52-52-52l-117.4 0c4-17-.6-35.5-13.8-48.8c-20.3-20.3-53.2-20.3-73.5 0L32 342.5 32 128c0-35.3 28.7-64 64-64zm64 64l-64 0 0 64c35.3 0 64-28.7 64-64zM544 320c-35.3 0-64 28.7-64 64l64 0 0-64zM320 352a96 96 0 1 0 0-192 96 96 0 1 0 0 192z"/>
      </svg>
    </div>
    <div class="expense-details">
      <h4>{{ expense.categories }}</h4>
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

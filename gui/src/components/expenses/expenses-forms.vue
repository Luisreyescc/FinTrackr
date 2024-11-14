<template>
  <div class="form-container">
    <h3>New expense data</h3>
    <form @submit.prevent="submitForm">
      <label>
        Amount:
        <input type="number" v-model="expense.amount" required />
      </label>
      <label>
	Description:
        <input type="text" v-model="expense.description" required />
      </label>
      <label>
        Categories:
        <input type="text" v-model="expense.categories" required />
      </label>
      <label>
        Date:
        <input type="date" v-model="expense.date" required />
      </label>
      <button type="submit">Submit Expense</button>
    </form>
  </div>
</template>

<script>
export default {
  name: "ExpensesForm",
  data() {
    return {
      expense: { amount: '', description: '', categories: '', date: '' }
    };
  },
  methods: {
    submitForm() {
      //this.$emit('submitForm', this.expense);
      this.$emit('submitForm', { ...this.expense });
      this.resetForm();
    },
    resetForm() {
      this.expense = { amount: '', description: '', categories: '', date: '' }
    }
  }
};
</script>

<style scoped>
.form-container {
  padding: 20px;
  border-radius: 8px;
}

label {
  display: block;
  margin-bottom: 10px;
  font-weight: bold;
  color: #333;
}

input {
  width: 100%;
  padding: 8px;
  margin-top: 5px;
  margin-bottom: 15px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.submit-button {
  background-color: #0F612F;
  color: white;
  border: none;
  padding: 10px 15px;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
}

.submit-button:hover {
  background-color: #237242;
}
</style>

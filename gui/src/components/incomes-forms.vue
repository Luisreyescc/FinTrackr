<template>
  <div class="form-container">
    <h3>New income data</h3>
    <form @submit.prevent="submitForm">
      <label>
        Amount:
        <input type="number" v-model="income.amount" required />
      </label>
      <label>
        Source:
        <input type="text" v-model="income.source" required />
      </label>
      <label>
      Description:
        <input type="text" v-model="income.description" required />
      </label>
      <label>
        Date:
        <input type="date" v-model="income.date" required />
      </label>
      <button type="submit">Submit Income</button>
    </form>
  </div>
</template>

<script>
export default {
  name: "IncomesForm",
  data() {
    return {
      income: { amount: '', description: '', source: '', date: '' }
    };
  },
  methods: {
    submitForm() {
      this.$emit('submitForm', this.income);
      this.resetForm();
    },
    resetForm() {
      this.income = { amount: '', description: '', source: '', date: '' };
    }
  }
};
</script>

<style scoped>
.form-container {
  padding: 10px;
}

label {
  display: block;
  margin: 10px 0;
}

button {
  background-color: #0F612F;
  color: white;
  border: none;
  padding: 10px 15px;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background-color: #237242;
}
</style>

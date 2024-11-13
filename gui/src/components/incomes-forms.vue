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
      income: { amount: '', source: '', description: '', date: '' }
    };
  },
  methods: {
    submitForm() {
      this.$emit('submitForm', this.income);
      this.resetForm();
    },
    resetForm() {
      this.income = { amount: '', source: '', description: '', date: '' };
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

/* Botón de envío del formulario */
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

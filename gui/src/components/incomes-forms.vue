<template>
  <div class="form-container">
    <h3 class="form-title">New Income Data</h3>
    <form @submit.prevent="submitForm">
      <label>
        Amount:
        <input
	  type="number"
	  v-model="income.amount"
          @input="validateAmount"
          :class="{ 'input-error': amountError, 'padded-input': true }"
          placeholder="Enter amount (e.g., 1000.00)" />
      </label>
      <span v-if="amountError" class="error-message">{{ amountError }}</span>
      
      <label>
        Source:
        <input type="text" v-model="income.source" @input="validateInput('source')" required />
      </label>
      <label>
      Description:
        <input type="text" v-model="income.description" @input="validateInput('description')" required />
      </label>
      <label>
        Date:
        <input type="date" v-model="income.date" required />
      </label>
      <div class="button-group">
        <button type="button" @click="cancelForm" class="cancel-button">Cancel</button>
        <button type="submit" class="submit-button">Submit Income</button>
      </div>
    </form>
  </div>
</template>

<script>
export default {
  name: "IncomesForm",
  data() {
    return {
      income: { amount: '', source: '', description: '', date: '' },
      validation: { amount: null, source: null, description: null }
    };
  },
  methods: {
    submitForm() {
      //this.$emit('submitForm', this.income);
      this.$emit('submitForm', { ...this.income });
      this.resetForm();
    },
    cancelForm() {
      this.resetForm();
      this.$emit('closeForm');
    },
    resetForm() {
      this.income = { amount: '', source: '', description: '', date: '' };
      this.validation = { amount: null, source: null, description: null };
    },
    validateInput(field) {
      this.validation[field] = this.income[field] ? 'valid' : 'invalid';
    }
  }
};
</script>

<style scoped>
.form-container {
    padding: 20px;
    border-radius: 8px;
    font-family: "Wix Madefor Display", sans-serif;
}

.form-title {
    font-size: 22px;
    font-weight: bold;
    color: #333;
    text-align: left;
    margin-bottom: 20px;
    font-family: "Wix Madefor Display", sans-serif;
}

label {
    display: block;
    margin-bottom: 10px;
    font-weight: bold;
    font-size: 18px;
    color: #333;
    text-align: left;
    font-family: "Wix Madefor Display", sans-serif;
}

input {
    width: 90%;
    padding: 14px;
    margin-top: 5px;
    margin-bottom: 15px;
    border: none;
    background-color: #f0f0f0;
    border-radius: 4px 4px 0 0;
    border-bottom: 2px solid #ccc;
    transition: background-color 0.3s, border-color 0.3s;
    font-family: "Wix Madefor Display", sans-serif;
}

input:focus {
    outline: none;
    background-color: #e0e0e0;
}

input.valid {
    background-color: #e0f7fa; 
    border-bottom-color: #00bcd4;
}

input.invalid {
    background-color: #ffebee;
    border-bottom-color: #d32f2f;
}

.button-group {
    display: flex;
    gap: 10px;
    justify-content: space-between;
}

.cancel-button {
    background-color: #757575;
    color: white;
    border: none;
    padding: 10px 15px;
    border-radius: 5px;
    cursor: pointer;
    font-weight: bold;
    font-family: "Wix Madefor Display", sans-serif;
}

.submit-button {
    background-color: #0f612f;
    color: white;
    border: none;
    padding: 10px 15px;
    border-radius: 5px;
    cursor: pointer;
    font-weight: bold;
    font-family: "Wix Madefor Display", sans-serif;
}

.cancel-button:hover {
    background-color: #616161;
}

.submit-button:hover {
    background-color: #237242;
}
</style>

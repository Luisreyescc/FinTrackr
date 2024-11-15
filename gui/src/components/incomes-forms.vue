<template>
<div class="form-container">
  <h3 class="form-title">New Income Data</h3>
  <form @submit.prevent="submitForm">
    <label>
      Amount:
      <input
	type="text"
	v-model="income.amount"
	@input="validateAmount"
	:class="{ 'input-error': amountError, 'input-valid': !amountError && income.amount }"
	placeholder="Enter amount (e.g., 1000.00)" />
    </label>
    <span v-if="amountError" class="error-message">{{ amountError }}</span>
    
    <label>
      Source:
      <input
	type="text"
	v-model="income.source"
	@input="validateTextField('source')"
	:class="{ 'input-error': sourceError, 'input-valid': !sourceError && income.source }"
	placeholder="Enter the source of the income" />
    </label>
    <span v-if="sourceError" class="error-message">{{ sourceError }}</span>
    
    <label>
      Description:
      <input
	type="text"
	v-model="income.description"
	@input="validateTextField('description')"
	:class="{ 'input-error': descriptionError, 'input-valid': !descriptionError && income.description }"
        placeholder="Enter a description for the income" />
    </label>
    <span v-if="descriptionError" class="error-message">{{ descriptionError }}</span>
      
    <label>
      Date:
      <input
	type="date"
        v-model="income.date"
        @input="validateDate"
        :class="{ 'input-error': dateError, 'input-valid': !dateError && income.date }" />
    </label>
    <span v-if="dateError" class="error-message">{{ dateError }}</span>
    
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
      amountError: "",
      sourceError: "",
      descriptionError: "",
      dateError: ""
    };
  },
  methods: {
    submitForm() {
      this.clearErrors();

      const isAmountValid = this.validateAmount();
      const isSourceValid = this.validateTextField('source');
      const isDescriptionValid = this.validateTextField('description');
      const isDateValid = this.validateDate();
      
      if (isAmountValid && isSourceValid && isDescriptionValid && isDateValid) {
	this.$emit('submitForm', { ...this.income });
	this.$emit('closeForm');
	this.resetForm();
      }
    },
    clearErrors() {
      this.amountError = "";
      this.sourceError = "";
      this.descriptionError = "";
      this.dateError = "";
    },
    cancelForm() {
      this.resetForm();
      this.$emit('closeForm');
    },
    resetForm() {
      this.income = { amount: '', source: '', description: '', date: '' };
      this.clearErrors();
    },
    validateAmount() {
      this.amountError = "";
      const amountPattern = /^\d{1,10}(\.\d{0,2})?$/; // Maximum of 10 digits before dot and 2 after it
      if (!this.income.amount) {
        this.amountError = "Amount is required";
        return false;
      }
      if (!amountPattern.test(this.income.amount)) {
        this.amountError = "Invalid amount format";
        return false;
      }
      return true;
    },
    validateTextField(field) {
      //function to determine the label error
      this[`${field}Error`] = "";
      if (!this.income[field]) {
        this[`${field}Error`] = `${field.charAt(0).toUpperCase() + field.slice(1)} is required`;
        return false;
      }
      if (this.income[field].length > 180) {
        this[`${field}Error`] = "Exceeded the maximum character limit of 180";
        return false;
      }
      return true;
    },
    validateDate() {
      this.dateError = "";
      if (!this.income.date) {
        this.dateError = "Date is required";
        return false;
      }
      return true;
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
    color: #21255b;
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
    margin-top: 10px;
    margin-bottom: 2px;
    border: none;
    outline: none;
    background-color: #f0f0f0;
    border-radius: 4px 4px 0 0;
    border-bottom: 2px solid #ccc;
    transition: background-color 0.3s, border-color 0.3s;
    font-family: "Wix Madefor Display", sans-serif;
}

.input-error {
  border-bottom-color: #e42121;
  background-color: #ffebee;
  outline: none;
}

.input-valid {
  border-bottom-color: #1B1F9C;
  background-color: #e0f7fa;
  outline: none;
}

.error-message {
  color: #e42121;
  font-size: 12px;
  margin-top: -10px;
  margin-bottom: 10px;
  text-align: left;
}

.button-group {
    display: flex;
    gap: 10px;
    margin-top: 55px;
    justify-content: space-between;
}

.cancel-button {
    background-color: #333;
    color: white;
    border: none;
    padding: 10px 15px;
    border-radius: 8px;
    cursor: pointer;
    font-weight: bold;
    font-family: "Wix Madefor Display", sans-serif;
}

.submit-button {
    background-color: #4caf50;
    color: white;
    border: none;
    padding: 10px 15px;
    border-radius: 8px;
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

<template>
<div class="form-container">
  <h3 class="form-title">New Expense data</h3>
  <div class="form-content scrollbar">
  <form @submit.prevent="submitForm">
    <label>
      Amount:
      <input type="text" v-model="expense.amount" @input="validateAmount" :class="{ 'input-error': amountError, 'input-valid': !amountError && expense.amount }" placeholder="Enter amount (e.g., 1000.00)" />
    </label>
    <span v-if="amountError" class="error-message">{{ amountError }}</span>
    
    <label>
      Description:
      <input type="text" v-model="expense.description" @input="validateTextField('description')" :class="{ 'input-error': descriptionError, 'input-valid': !descriptionError && expense.description }" placeholder="Enter a description for the expense" />
    </label>
    <span v-if="descriptionError" class="error-message">{{ descriptionError }}</span>
    
    <div class="categories-wrapper">
      <div class="categories-select" @click="toggleDropdown">
        Categories
        <span class="dropdown-icon">
	<svg v-if="!dropdownOpen" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 512">
	<path d="M278.6 233.4c12.5 12.5 12.5 32.8 0 45.3l-160 160c-12.5 12.5-32.8 12.5-45.3 0s-12.5-32.8 0-45.3L210.7 256 73.4 118.6c-12.5-12.5-12.5-32.8 0-45.3s32.8-12.5 45.3 0l160 160z" />
        </svg>
	<svg v-else xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512">
                <path d="M201.4 374.6c12.5 12.5 32.8 12.5 45.3 0l160-160c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0L224 306.7 86.6 169.4c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3l160 160z" />
              </svg>
	</span>
      </div>
      
      <ul v-if="dropdownOpen" class="categories-dropdown scrollbar">
        <li
          v-for="(category, index) in categoryOptions"
          :key="index"
          @click="addCategory(category)">{{ category }}</li></ul>
      
      <div class="selected-categories">
        <span v-for="(category, index) in expense.categories" :key="index" class="tag">
          {{ category }}
	<button @click="removeCategory(index)" class="close-button">
            <span class="gg-close"></span>
          </button>
        </span>
      </div>
    </div>
    
    <label>
      Date:
      <input
        type="date"
        v-model="expense.date"
        @input="validateDate"
        :class="{ 'input-error': dateError, 'input-valid': !dateError && expense.date }" />
    </label>
    <span v-if="dateError" class="error-message">{{ dateError }}</span>
    
    <div class="button-group">
      <button type="button" @click="cancelForm" class="cancel-button">Cancel</button>
      <button type="submit" class="submit-button">Submit</button>
    </div>
  </form>
  </div>
</div>
</template>

<script>
import '@/css/scrollbar.css';
 
export default {
  name: "ExpensesForm",
  data() {
    return {
      expense: { amount: '', description: '', categories: [], date: '' },
      amountError: "",
      descriptionError: "",
      dateError: "",
      categoryOptions: [
	"Food",
	"Travel",
	"Utilities",
	"Rent",
	"Entertainment",
	"Shopping",
	"Education",
	"Health"],
      dropdownOpen: false,
    };
  },
  methods: {
    submitForm() {
      this.clearErrors();

      const isAmountValid = this.validateAmount();
      const isDescriptionValid = this.validateTextField('description');
      const isDateValid = this.validateDate();
      
      if (isAmountValid && isDescriptionValid && isDateValid) {
	this.$emit('submitForm', { ...this.expense });
	this.$emit('closeForm');
	this.resetForm();
      }
    },
    toggleDropdown() {
      this.dropdownOpen = !this.dropdownOpen;
    },
    addCategory(category) {
      if (!this.expense.categories.includes(category)) {
        this.expense.categories.push(category);
      }
      this.dropdownOpen = false;
    },
    removeCategory(index) {
      this.expense.categories.splice(index, 1);
    },
    clearErrors() {
      this.amountError = "";
      this.descriptionError = "";
      this.categoriesError = "";
      this.dateError = "";
    },
    cancelForm() {
      this.resetForm();
      this.$emit('closeForm');
    },
    resetForm() {
      this.expense = { amount: '', description: '', categories: [], date: '' };
      this.dropdownOpen = false;
      this.clearErrors();
    },
    validateAmount() {
      this.amountError = "";
      const amountPattern = /^\d{1,10}(\.\d{0,2})?$/;
      if (!this.expense.amount) {
        this.amountError = "Amount is required";
        return false;
      }
      if (!amountPattern.test(this.expense.amount)) {
        this.amountError = "Invalid amount format";
        return false;
      }
      return true;
    },
    validateTextField(field) {
      //function to determine the label error
      this[`${field}Error`] = "";
      if (!this.expense[field]) {
        this[`${field}Error`] = `${field.charAt(0).toUpperCase() + field.slice(1)} is required`;
        return false;
      }
      if (this.expense[field].length > 180) {
        this[`${field}Error`] = "Exceeded the maximum character limit of 180";
        return false;
      }
      return true;
    },
    validateDate() {
      this.dateError = "";
      if (!this.expense.date) {
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
    box-sizing: border-box;
}

.form-title {
    font-size: 22px;
    font-weight: bold;
    color: #333;
    text-align: left;
    margin-bottom: 40px;
    color: #21255b;
    font-family: "Wix Madefor Display", sans-serif;
}

.form-content {
    max-height: calc(80vh - 220px);
    padding: 10px;
    margin: 0;
    overflow-y: auto;
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
    margin-top: 80px;
    justify-content: space-between;
}

.cancel-button {
    background-color: #333;
    color: white;
    border: none;
    padding: 13px 30px;
    border-radius: 2px;
    cursor: pointer;
    font-size: 16px;
    font-weight: bold;
    font-family: "Wix Madefor Display", sans-serif;
}

.submit-button {
    background-color: #4caf50;
    color: white;
    border: none;
    padding: 13px 30px;
    border-radius: 3px;
    cursor: pointer;
    font-size: 16px;
    font-weight: bold;
    font-family: "Wix Madefor Display", sans-serif;
}

.cancel-button:hover {
    background-color: #616161;
}

.submit-button:hover {
    background-color: #237242;
}

.categories-wrapper {
    position: relative;
    margin-bottom: 20px;
    font-family: "Wix Madefor Display", sans-serif;
}

.categories-select {
    padding: 12px 15px;
    border: 1px solid #ccc;
    border-radius: 8px;
    cursor: pointer;
    display: flex;
    align-items: center;
    width: 110px;
    font-weight: bold;
    background-color: #ffffff;
    box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1);
    transition: background-color 0.2s;
}

.categories-select:hover {
    background-color: #f8f9fa;
}

.dropdown-icon svg {
    top: 5px;
    width: 16px;
    height: 16px;
    margin-left: 8px;
    transform: translateY(3px);
    color: #21255b;
}

.categories-dropdown {
    position: absolute;
    top: 80%;
    left: 0;
    right: 0;
    border: 1px solid #ddd;
    border-radius: 12px;
    background-color: white;
    box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
    padding: 0;
    list-style: none;
    z-index: 1000;
    overflow-y: auto;
    max-height: 160px;
    max-width: 200px;
    animation: fadeIn 0.2s ease-out;
}

.categories-dropdown li {
    padding: 10px 20px;
    cursor: pointer;
    transition: background-color 0.3s, color 0.3s;
    text-align: left;
}

.categories-dropdown li:hover {
    background-color: #f0f8ff;
    border-radius: 12px;
    color: #1010AC;
    font-weight: bold;
}

.selected-categories {
    margin-top: 10px;
    display: flex;
    flex-wrap: wrap;
    gap: 5px;
}

.tag {
    background-color: #F3F3F9;
    border: 1px solid #6F6F7A;
    border-radius: 16px;
    padding: 5px 10px;
    display: flex;
    font-weight: bold;
    align-items: center;
}

.close-button {
    background: none;
    border: none;
    cursor: pointer;
    margin-right: -10px;
}

.close-button .gg-close {
    font-size: 12px;
    color: #333;
}
</style>

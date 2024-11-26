<template>
<div class="form-container">
  <h3 class="form-title">New Expense data</h3>
  <div class="form-content scrollbar">
  <form @submit.prevent="submitForm">
    <label>
      Amount:
      <input
	type="text"
	v-model="expense.amount"
	@input="validateAmount"
	:class="{ 'input-error': amountError, 'input-valid': !amountError && expense.amount }"
	placeholder="Enter amount (e.g., 1000.00)" />
    </label>
    <span v-if="amountError" class="error-message">{{ amountError }}</span>
    
    <label>
      Description:
      <input
	type="text"
	v-model="expense.description"
	@input="validateTextField('description')"
	:class="{ 'input-error': descriptionError, 'input-valid': !descriptionError && expense.description }"
	placeholder="Enter a description for the expense" />
    </label>
    <span v-if="descriptionError" class="error-message">{{ descriptionError }}</span>
    
    <div class="categories-wrapper">
      <div class="categories-select" @click="toggleDropdown">
        Categories
        <span class="dropdown-icon">
	<font-awesome-icon v-if="!dropdownOpen" :icon="['fas', 'angle-right']" />
	<font-awesome-icon v-else :icon="['fas', 'angle-down']" />
	</span>
      </div>
      
      <ul v-if="dropdownOpen" class="categories-dropdown scrollbar">
	<li @click="showNewCategoryDialog" style="color: green; font-weight: bold;">
          <font-awesome-icon :icon="['fas', 'plus']" font-size="12" /> New category
	</li>
        <li
          v-for="(category, index) in categoryOptions"
          :key="index"
          @click="newCategory(category)">{{ category }}
	</li>
      </ul>

      <div v-if="showNewCategory" class="overlay" @click="cancelNewCategory"></div>
      <div v-if="showNewCategory" class="new-category-dialog">
	<h4>Enter new category</h4>
	<input
          type="text"
          v-model="newCategory"
          placeholder="New category"
          :maxlength="18" />
	<div class="button-group">
          <button @click="cancelNewCategory" class="cancel-category">Cancel</button>
          <button
            @click="acceptNewCategory"
            class="accept-category"
            :disabled="!isAcceptEnabled">Accept</button>
	</div>
      </div>
      
      <div class="selected-categories">
         <span v-for="(category, index) in expense.categories" :key="index" class="tag">
           {{ category }}
           <button @click="removeCategory(index)" class="close-button">
             <font-awesome-icon :icon="['fas', 'xmark']"/>
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
      <button type="submit" class="submit-button" :disabled="!isSubmitEnabled">Submit</button>
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
	"Groceries",
	"Food",
	"Travel",
	"Utilities",
	"Rent",
	"Entertainment",
	"Shopping",
	"Education",
	"Health",
	"Transportation",
	"Bills",
	"Taxes"],
      dropdownOpen: false,
      showNewCategory: false,
      newCategory: "",
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
    showNewCategoryDialog() {
      this.newCategory = "";
      this.showNewCategory = true;
    },
    cancelNewCategory() {
      this.showNewCategory = false;
    },
    acceptNewCategory() {
      if (this.newCategory.trim()) {
        if (!this.categoryOptions.includes(this.newCategory)) {
          this.categoryOptions.push(this.newCategory);
        }
        this.expense.categories.push(this.newCategory);
        this.showNewCategory = false;
        this.newCategory = "";
	this.dropdownOpen = false;
      }
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
  },
  computed: {
    isSubmitEnabled() {
      return this.expense.categories.length > 0;
    },
    isAcceptEnabled() {
      return this.newCategory.trim().length > 0;
    },
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

.dropdown-icon {
    width: 16px;
    height: 16px;
    margin-left: 8px;
    transform: translateY(-1px);
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
    display: flex;
    flex-wrap: wrap;
    margin-top: 10px;
    gap: 5px;
}

.tag {
    display: flex;
    align-items: center;
    border-radius: 16px;
    padding: 5px 10px;
    font-weight: bold;
    background-color: #F3F3F9;
    border: 1px solid #6F6F7A;
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

.new-category-dialog {
    position: fixed;
    background: white;
    border: 1px solid #ccc;
    border-radius: 8px;
    padding: 15px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    z-index: 1100;
    width: 220px;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
}

.new-category-dialog h4 {
  margin: 0 0 10px;
  font-size: 18px;
  color: #21255b;
  font-family: "Wix Madefor Display", sans-serif;
}

.new-category-dialog input {
    width: 90%;
    padding: 14px;
    margin-top: 10px;
    border: none;
    outline: none;
    background-color: #f0f0f0;
    border-radius: 4px 4px 0 0;
    border-bottom: 2px solid #ccc;
    transition: background-color 0.3s, border-color 0.3s;
    font-family: "Wix Madefor Display", sans-serif;
}

.new-category-dialog .button-group {
    display: flex;
    justify-content: space-between;
    margin-top: 15px;
}

.cancel-category, .accept-category {
    color: white;
    border: none;
    padding: 8px 18px;
    border-radius: 2px;
    cursor: pointer;
    font-size: 14px;
    font-weight: bold;
    font-family: "Wix Madefor Display", sans-serif;
}

.cancel-category {
    background-color: #333; 
}

.accept-category {
    background-color: #4caf50; 
}

.cancel-button:hover {
    background-color: #616161;
}

.submit-button:hover {
    background-color: #237242;
}

.submit-button:disabled,
.accept-category:disabled {
    background-color: #A2CBB2;
    cursor: not-allowed;
    opacity: 0.7;
}
</style>

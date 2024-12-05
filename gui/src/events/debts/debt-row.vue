<template>
<div class="debt-row">
  <div class="debt-checkbox">
    <input type="checkbox" :checked="isChecked" @change="toggleDebtChecked" class="checkbox"/>
  </div>
  <div class="debt-details">
    <h4>{{ formattedCategories }}</h4>
    <p class="debt-description">{{ debt.description }}</p>
    <span class="debt-date">{{ formattedDate }}</span>
  </div>
  <div class="debt-amount-section">
    <span class="debt-amount">{{ formattedAmount }}</span>
    <div class="debt-actions">
      <button class="edit-button" @click="startEdit">
        <font-awesome-icon :icon="['fas', 'pen-to-square']" class="edit-icon"/>
      </button>
      <button class="delete-button" @click="deleteDebt">
	<font-awesome-icon :icon="['fas', 'trash-can']" class="trash-icon"/>
      </button>
    </div>
  </div>
</div>

<div v-if="isEditing" class="overlay" @click="cancelEdit"></div>
<div v-if="isEditing" class="edit-popup">
  <h3 class="edit-title">Edit Debt</h3>
  <div class="popup-content">
    <form @submit.prevent="submitEdit">
      <label>
        Amount:
        <input
          type="text"
          v-model="editExpense.amount"
          @input="validateAmount"
          :class="{ 'input-error': amountError, 'input-valid': !amountError && editExpense.amount }"
          placeholder="Enter amount (e.g., 1000.00)"/>
      </label>
      <span v-if="amountError" class="error-message">{{ amountError }}</span>
      
      <label>
        Description:
        <input
          type="text"
          v-model="editDebt.description"
          @input="validateTextField('description')"
          :class="{ 'input-error': descriptionError, 'input-valid': !descriptionError && editDebt.description }"
          placeholder="Enter a description for the debt"/>
      </label>
      <span v-if="descriptionError" class="error-message">{{ descriptionError }}</span>
      
      <div class="categories-wrapper">
	<div class="categories-select" @click="toggleDropdown">
          Categories
          <span class="dropdown-icon">
            <font-awesome-icon v-if="!dropdownOpen" :icon="['fas', 'angle-right']"/>
            <font-awesome-icon v-else :icon="['fas', 'angle-down']"/>
          </span>
	</div>
	
	<ul v-if="dropdownOpen" class="categories-dropdown scrollbar">
          <li v-if="loadingCategories">Loading categories...</li></ul>
	
	<div class="selected-categories">
          <span v-for="(category, index) in expense.categories" :key="index" class="tag">
            {{ category }}
            <button @click="removeCategory(index)" class="close-button">
              <font-awesome-icon :icon="['fas', 'xmark']"/>
            </button>
          </span>
	</div>
      </div>
      
      <label class="date-label">
        Date:
      </label>
      <div class="date-container">
        <font-awesome-icon class="birth-icon" :icon="['fas', 'calendar']"/>
        <input
          v-model="editDebt.date"
          type="date"
          @input="validateDate"
          class="custom-date-input"
          :class="{ 'input-error': dateError, 'input-valid': !dateError && editDebt.date }"/>
      </div>
      <span v-if="dateError" class="error-message">{{ dateError }}</span>
      
      <div class="button-group">
        <button type="button" class="cancel-button" @click="cancelEdit">Cancel</button>
	<button type="submit" class="submit-button" :disabled="!isSubmitEnabled">Save</button>
      </div>
    </form>
  </div>
</div>
</template>

<script>
import '@/css/scrollbar.css';
import axios from 'axios';

export default {
  name: "DebtRow",
  props: {
    debt: {
      type: Object,
      required: true,
      default: () => ({ categories: [], isChecked: false })
    }
  },
  data() {
    return {
      isEditing: false,
      isChecked: this.debt.isChecked,
      editDebt: {
        ...this.debt, 
        categories: this.debt.categories || [] 
      },
      amountError: "",
      descriptionError: "",
      dateError: "",
      categoryOptions: [],
      dropdownOpen: false,
      showNewCategory: false,
      newCategory: "",
      loadingCategories: false
    };
  },
  computed: {
    formattedAmount() {
      // This for give the amount format in USD
      const formatter = new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
      });
      return `${formatter.format(this.expense.amount)}`;
    },
    formattedCategories() {
      return this.debt.categories ? this.debt.categories.join(", ") : "No categories";
    },
    formattedDate() {
      // Data format day-MONTH-year
      const date = new Date(this.debt.date);
      const day = String(date.getDate()).padStart(2, '0');
      const month = date.toLocaleString('en-US', { month: 'short' }).toUpperCase();
      const year = date.getFullYear();
      return `${year}-${month}-${day}`;
    },
    isSubmitEnabled() {
      return this.debt.categories.length > 0;
    },
    isAcceptEnabled() {
      return this.newCategory.trim().length > 0;
    },
  },
  methods: {
    startEdit() {
      this.isEditing = true;
      this.editDebt = { ...this.debt };
    },
    cancelEdit() {
      this.isEditing = false;
      this.editDebt = { ...this.debt };
      this.clearErrors();
    },
    clearErrors() {
      this.amountError = "";
      this.descriptionError = "";
      this.dateError = "";
    },
    toggleDropdown() {
      this.dropdownOpen = !this.dropdownOpen;
    },
    submitEdit() {
      this.clearErrors();
      
      const isAmountValid = this.validateAmount();
      const isDescriptionValid = this.validateTextField("description");
      const isDateValid = this.validateDate();

      if (isAmountValid && isDescriptionValid && isDateValid) {
        this.$emit("updateDebt", this.editDebt);
        this.isEditing = false;
      }
    },
    async fetchCategories() {
      try {
        const token = localStorage.getItem("token");
        if (!token) {
          console.error("No token found");
          return;
        }

        this.loadingCategories = true;
        const response = await axios.get('http://localhost:8000/api/user-categories/', {
          headers: { Authorization: `Bearer ${token}` },
        });
        this.categoryOptions = response.data.categories;
      } catch (error) {
        console.error("Error fetching categories:", error);
      } finally {
        this.loadingCategories = false;
      }
    },
    async sendNewCategory() {
      try {
        const response = await axios.post('http://localhost:8000/api/categories/', { name: this.newCategory.trim() });
        if (response.status === 201) {
          // Add new category to the user's categories table if the backend respons with success
          this.categoryOptions.push(this.newCategory.trim());
          this.editDebt.categories.push(this.newCategory.trim());
        } else {
          console.error("Failed to add category:", response.statusText);
        }
      } catch (error) {
        console.error("Error adding new category:", error);
      }
    },
    async acceptNewCategory() {
      if (this.newCategory.trim()) {
        await this.sendNewCategory();
        this.editDebt.categories.push(this.newCategory);
        this.showNewCategory = false;
        this.newCategory = "";
	this.dropdownOpen = false;
      }
    },
    async toggleDebtChecked(event) {
      this.isChecked = event.target.checked;
      try {
        const token = localStorage.getItem("token");
        if (!token) {
          console.error("No token found");
          return;
        }
	const response = await axios.patch(
          `http://localhost:8000/api/debts/${this.expense.id}/`,
          { is_checked: this.isChecked },
          { headers: { Authorization: `Bearer ${token}` } }
        );
	console.log("Debt updated:", response.data);
      } catch (error) {
        console.error("Error updating debt:", error);
      }
    },
    addCategory(category) {
      if (!this.editDebt.categories.includes(category)) {
        this.editDebt.categories.push(category);
	this.newCategory = "";
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
    removeCategory(index) {
      this.editDebt.categories.splice(index, 1);
    },
    validateAmount() {
      const amountPattern = /^\d{1,10}(\.\d{0,2})?$/;
      if (!this.editDebt.amount) {
        this.amountError = "Amount is required";
        return false;
      }
      if (!amountPattern.test(this.editDebt.amount)) {
        this.amountError = "Invalid amount format";
        return false;
      }
      return true;
    },
    validateTextField(field) {
      this[`${field}Error`] = "";
      if (!this.editDebt[field]) {
        this[`${field}Error`] = `${field.charAt(0).toUpperCase() + field.slice(1)} is required`;
        return false;
      }
      if (this.editDebt[field].length > 180) {
        this[`${field}Error`] = "Exceeded the maximum character limit of 180";
        return false;
      }
      return true;
    },
    validateDate() {
      if (!this.editDebt.date) {  // Corrected this line
        this.dateError = "Date is required";
        return false;
      }
      return true;
    },
    deleteDebt() {
      console.log("Removing debt");
      this.$emit("deleteDebt", this.debt.debt_id);
    }
  },
  mounted() {
    this.fetchCategories();
  },
};
</script>

<style scoped>
.debt-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 15px;
    background: #25262B;
    border: 2px solid white;
    border-radius: 20px;
    margin-bottom: 10px;
    box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1);
}

.checkbox {
    width: 20px;
    height: 20px;
    accent-color: #25262B;
    border: 1px solid #ccc;
    border-radius: 4px;
    cursor: pointer;
}

.checkbox:checked {
    background-color: #25262B;
}

.debt-details {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    overflow: hidden;
}

.debt-details h4, .debt-description {
    margin: 0;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 420px;
    margin-left: 10px;
}

.debt-details h4 {
    font-size: 22px;
    color: #6092DE;
    font-weight: bold;
}

.debt-description {
    color: white;
    font-weight: bold;
    font-size: 20px;
}

.debt-date {
    color: #BF9F00;
    font-weight: bold;
    font-size: 18px;
    margin-left: 10px;
    white-space: nowrap;
}

.debt-amount-section {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    margin-left: 25px;
    margin-top: 5px;
}

.debt-amount {
    font-weight: bold;
    color: #6092DE;
    font-size: 20px;
    flex-shrink: 0;
}

.debts-actions {
    display: flex;
    gap: 10px;
    margin-top: 5px;
}

.edit-button, .delete-button {
    border-radius: 10px;
    cursor: pointer;
    width: 38px;
    height: 38px;
    display: flex;
    align-items: center;
    justify-content: center;
    border: none;
    transition: transform 0.2s, background-color 0.2s;
}
.edit-button {
    background-color: white;
}

.edit-button:hover {
    transform: scale(1.1);
    background-color: #F2F2F2;
}

.delete-button {
    background-color: #D55C5C;
    color: white;
}

.delete-button:hover {
    transform: scale(1.1);
    background-color: darkred;
}

.edit-icon {
    font-size: 20px;
    color: #25262B;
}

.trash-icon {
    font-size: 20px;
    color: white;
}

.edit-popup {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background: #25262B;
    border-radius: 12px;
    box-shadow: 0 4px 10px rgba(255, 255, 255, 0.1);
    padding: 20px;
    width: 600px;
    z-index: 1000;
}

.popup-content {
    display: flex;
    flex-direction: column;
}

.overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: rgba(59, 59, 90, 0.5);
    backdrop-filter: blur(3px);
    z-index: 1000;
}

.edit-title {
    font-size: 28px;
    font-weight: bold;
    text-align: center;
    margin-bottom: 20px;
    color: white;
    font-family: "Wix Madefor Display", sans-serif;
}

label {
    display: block;
    margin-bottom: 10px;
    font-weight: bold;
    font-size: 24px;
    color: white;
    text-align: left;
    font-family: "Wix Madefor Display", sans-serif;
}

input {
    width: 93%;
    padding: 20px;
    margin-top: 10px;
    margin-bottom: 2px;
    border: none;
    outline: none;
    color: white;
    font-size: 18px;
    background-color: #25262B;
    border-radius: 4px;
    border: 2px solid white;
    transition: background-color 0.3s, border-color 0.3s;
    font-family: "Wix Madefor Display", sans-serif;
}

input::placeholder {
    color: white;
    font-size: 16px;
}

.input-error {
    border-color: #D55C5C;
    outline: none;
}

.input-valid {
    outline: none;
}

input[type="date"] {
    color: white;
    font-size: 16px;
    font-family: "Wix Madefor Display", sans-serif;
}

input[type="date"]::-webkit-calendar-picker-indicator {
    color: white;
    cursor: pointer;
}

input[type="date"]::-webkit-calendar-picker-indicator:hover {
    color: white;
}

.error-message {
    color: #D55C5C;
    font-size: 16px;
    margin-top: -10px;
    margin-bottom: 10px;
    text-align: left;
}

.button-group {
    display: flex;
    gap: 10px;
    justify-content: space-between;
    margin-top: 50px;
}

.cancel-button {
    background-color: #25262B;
    color: white;
    border: 2px solid white;
    padding: 15px 35px;
    border-radius: 20px;
    cursor: pointer;
    font-size: 16px;
    font-weight: bold;
    font-family: "Wix Madefor Display", sans-serif;
}

.submit-button {
    background-color: white;
    color: #25262B;
    border: none;
    padding: 15px 35px;
    border-radius: 20px;
    cursor: pointer;
    font-size: 16px;
    font-weight: bold;
    font-family: "Wix Madefor Display", sans-serif;
}

.cancel-button:hover {
    background-color: #333;
}

.submit-button:hover {
    background-color: #f8f9fa;
}

.categories-wrapper {
    position: relative;
    margin-top: 20px;
    margin-bottom: 20px;
    font-family: "Wix Madefor Display", sans-serif;
}

.categories-select {
    padding: 15px 30px;
    border: 1px solid #ccc;
    border-radius: 3px;
    cursor: pointer;
    display: flex;
    align-items: center;
    width: 115px;
    font-size: 18px;
    font-weight: bold;
    color: #25262B;
    background-color: white;
    box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1);
    transition: background-color 0.2s;
}

.categories-select:hover {
    background-color: #f8f9fa;
}

.dropdown-icon {
    width: 16px;
    height: 16px;
    margin-left: 16px;
    transform: translateY(-3px);
    color: #25262B;
}

.categories-dropdown {
    position: absolute;
    top: 80%;
    left: 0;
    right: 0;
    border: 1px solid #3F4049;
    border-radius: 12px;
    background-color: #404149;
    box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
    padding: 0;
    list-style: none;
    z-index: 1000;
    overflow-y: auto;
    overflow-x: hidden;
    max-height: 160px;
    max-width: 250px;
    animation: fadeIn 0.2s ease-out;
}

.categories-dropdown li {
    padding: 10px 20px;
    cursor: pointer;
    transition: background-color 0.3s, color 0.3s;
    text-align: left;
    color: white;
    font-weight: bold;
}

.categories-dropdown li:hover {
    background-color: white;
    border-radius: 12px;
    color: #25262B;
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
    padding: 8px 20px;
    font-weight: bold;
    color: #25262B;
    background-color: white;
    border: 1px solid white;
}

.close-button {
    background: none;
    border: none;
    cursor: pointer;
    margin-top: 2px;
    margin-right: -15px;
}

.close-button .gg-close {
    font-size: 18px;
    color: #25262B;
}

.new-category-dialog {
    position: fixed;
    background: white;
    border: 1px solid white;
    border-radius: 8px;
    padding: 15px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    z-index: 1100;
    width: 400px;
    height: 230px;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
}

.new-category-dialog h4 {
    margin-top: 15px;
    font-size: 22px;
    color: #25262B;
    font-family: "Wix Madefor Display", sans-serif;
}

.new-category-dialog input {
    width: 90%;
    padding: 14px;
    margin-bottom: 2px;
    border: none;
    outline: none;
    color: #25262B;
    font-size: 18px;
    background-color: white;
    border-radius: 4px;
    border: 2px solid #25262B;
    transition: background-color 0.3s, border-color 0.3s;
    font-family: "Wix Madefor Display", sans-serif;
}

.new-category-dialog input::placeholder {
    color: #25262B;
}

.new-category-dialog .button-group {
    display: flex;
    justify-content: space-between;
    margin-top: 30px;
}

.cancel-category,
.accept-category {
    padding: 15px 30px;
    border: none;
    border-radius: 3px;
    cursor: pointer;
    font-size: 16px;
    font-weight: bold;
    font-family: "Wix Madefor Display", sans-serif;
}

.cancel-category {
    background-color: #25262B;
    color: white;
}

.accept-category {
    background-color: white;
    color: #25262B;
    border: 2px solid #25262B;
}

.submit-button:disabled,
.accept-category:disabled {
    background-color: #f8f9fa;
    cursor: not-allowed;
    opacity: 0.7;
}

.date-label {
    display: block;
    margin-bottom: 5px;
    margin-top: 15px;
    font-weight: bold;
    color: white;
    text-align: left;
    font-family: "Wix Madefor Display", sans-serif;
}

.date-container {
    left: 0px;
    position: relative;
    display: inline-block;
    width: 100%; 
}

.birth-icon {
    position: absolute;
    right: 23px;
    top: 50%;
    transform: translateY(-30%);
    color: white;
    pointer-events: none;
}

.date-container input[type="date"]::-webkit-calendar-picker-indicator {
    opacity: 0;
    cursor: pointer;
}
</style>

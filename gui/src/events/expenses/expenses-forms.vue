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
          placeholder="Enter amount (e.g., 1000.00)"/>
      </label>
      <span v-if="amountError" class="error-message">{{ amountError }}</span>
      
      <label>
        Description:
        <input
          type="text"
          v-model="expense.description"
          @input="validateTextField('description')"
          :class="{ 'input-error': descriptionError, 'input-valid': !descriptionError && expense.description }"
          placeholder="Enter a description for the expense"/>
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
          <li v-if="loadingCategories">Loading categories...</li>
          <li v-else @click="showNewCategoryDialog" style="color: #BF9F00; font-weight: bold">
            <font-awesome-icon :icon="['fas', 'plus']" font-size="12"/> New category
          </li>
          <li
            v-for="(category, index) in categoryOptions"
            :key="index"
            @click="addCategory(category)">{{ category }}
          </li>
        </ul>
	
        <div v-if="showNewCategory" class="overlay" @click="cancelNewCategory"></div>
        <div v-if="showNewCategory" class="new-category-dialog">
          <h4>Enter new category</h4>
          <input
            type="text"
            v-model="newCategory"
            placeholder="New category"
            :maxlength="18"/>
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
            <button type="button" @click="removeCategory(index, $event)" class="close-button">
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
          type="date"
          v-model="expense.date"
          @input="validateDate"
          class="custom-date-input"
          :class="{ 'input-error': dateError, 'input-valid': !dateError && expense.date }"/>
      </div>
      <span v-if="dateError" class="error-message">{{ dateError }}</span>

      <div class="icons-wrapper">
        <IconDropdown
          :iconOptions="iconOptions"
          :currentIcon="expense.icon"
          @iconSelected="applyIcon" />
        <span class="selected-text">Selected Icon: </span>
        <span v-if="expense.icon" class="selected-icon">
          <font-awesome-icon :icon="expense.icon"/>
        </span>
      </div>
      
      <div class="button-group">
        <button type="button" @click="cancelForm" class="cancel-button">Cancel</button>
        <button type="submit" class="submit-button" :disabled="!isSubmitEnabled">Submit</button>
      </div>
    </form>
  </div>
</div>
</template>

<script>
import "@/css/scrollbar.css";
import axios from "axios";
import IconDropdown from "@/components/icon-dropdown.vue";

export default {
  name: "ExpensesForm",
  components: {
    IconDropdown
  },
  data() {
    return {
      expense: { amount: "", description: "", categories: [], date: "", icon: "" },
      amountError: "",
      descriptionError: "",
      dateError: "",
      categoryOptions: [],
      dropdownOpen: false,
      showNewCategory: false,
      newCategory: "",
      loadingCategories: false,
      iconOptions: [
        ['fas', 'circle-dollar-to-slot'],
        ['fas', 'money-bill-transfer'],
        ['fas', 'piggy-bank'],
        ['fas', 'hand-holding-dollar'],
	['fas', 'credit-card'],
	['fas', 'handshake'],
	['fas', 'sack-dollar'],
	['fas', 'comments-dollar'],
	['fas', 'store'],
	['fas', 'shop'],
	['fas', 'cart-shopping'],
	['fas', 'bag-shopping'],
	['fas', 'suitcase-medical'],
	['fas', 'heart-pulse'],
	['fas', 'stethoscope'],
	['fas', 'syringe'],
	['fas', 'pills'],
	['fas', 'tooth'],
	['fas', 'hospital'],
	['fas', 'hand-holding-medical'],
	['fas', 'house-chimney'],
	['fas', 'gift'],
	['fas', 'heart'],
	['fas', 'dumbbell'],
	['fas', 'burger'],
	['fas', 'pizza-slice'],
	['fas', 'hotdog'],
	['fas', 'ice-cream'],
	['fas', 'utensils'],
	['fas', 'bowl-food'],
	['fas', 'drumstick-bite'],
	['fas', 'shrimp'],
	['fas', 'cake-candles'],
	['fas', 'mug-hot'],
	['fas', 'champagne-glasses'],
	['fas', 'martini-glass-citrus'],
	['fas', 'ferry'],
	['fas', 'car'],
	['fas', 'train-subway'],
	['fas', 'plane-departure'],
	['fas', 'hotel'],
	['fas', 'school'],
	['fas', 'building'],
	['fas', 'umbrella-beach'],
	['fas', 'gas-pump'],
	['fas', 'shirt'],
	['fas', 'film'],
	['fas', 'ticket'],
	['fas', 'gamepad'],
	['fas', 'mobile'],
	['fas', 'tv'],
	['fas', 'headphones-simple'],
	['fas', 'microphone'],
	['fas', 'video'],
	['fas', 'camera-retro'],
	['fas', 'music'],
	['fas', 'futbol'],
	['fas', 'person-swimming'],
	['fas', 'basketball'],
	['fas', 'bicycle'],
	['fab', 'youtube'],
	['fab', 'twitch'],
	['fab', 'steam'],
	['fab', 'spotify'],
	['fab', 'apple'],
	['fab', 'android'],
	['fab', 'xbox'],
	['fab', 'playstation'],
	['fab', 'docker'],
	['fab', 'linux'],
	['fab', 'gitlab'],
	['fab', 'github']
      ],
    };
  },
  methods: {
    submitForm() {
      this.clearErrors();

      const isAmountValid = this.validateAmount();
      const isDescriptionValid = this.validateTextField("description");
      const isDateValid = this.validateDate();

      if (isAmountValid && isDescriptionValid && isDateValid) {

        const iconString = this.expense.icon.join(' ');
        const expenseData = { ...this.expense, icon: iconString };

        this.$emit('submitForm', expenseData);
        this.$emit("closeForm");
        this.resetForm();
        this.fetchCategories();
      }
    },
    toggleDropdown() {
      this.dropdownOpen = !this.dropdownOpen;
    },
    async fetchCategories() {
      try {
        const token = localStorage.getItem("token");
        if (!token) {
          console.error("No token found");
          return;
        }

        this.loadingCategories = true;
        const response = await axios.get(
          "http://localhost:8000/api/expense-categories/",
          {
            headers: { Authorization: `Bearer ${token}` },
          },
        );
        this.categoryOptions = response.data.categories || [];
        this.categoryOptions = [...new Set(this.categoryOptions)];
      } catch (error) {
        console.error("Error fetching categories:", error);
      } finally {
        this.loadingCategories = false;
      }
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
        const newCategory = this.newCategory.trim();
        if (!this.categoryOptions.includes(newCategory)) {
          this.categoryOptions.push(newCategory);
        }
        if (!this.expense.categories.includes(newCategory)) {
          this.expense.categories.push(newCategory);
        }
        this.newCategory = "";
        this.showNewCategory = false;
        this.dropdownOpen = false;
      }
    },
    removeCategory(index, event) {
      event.stopPropagation();
      event.preventDefault(); // Prevent the default form submission
      this.expense.categories.splice(index, 1);
    },
    clearErrors() {
      this.amountError = "";
      this.descriptionError = "";
      this.dateError = "";
    },
    cancelForm() {
      this.resetForm();
      this.$emit("closeForm");
    },
    resetForm() {
      this.expense = { amount: "", description: "", categories: [], date: "" };
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
        this[`${field}Error`] =
          `${field.charAt(0).toUpperCase() + field.slice(1)} is required`;
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
    },
    applyIcon(selectedIcon) {
      this.expense.icon = selectedIcon;
    },
  },
  computed: {
    isSubmitEnabled() {
      return this.expense.categories.length > 0 && this.expense.icon;
    },
    isAcceptEnabled() {
      return this.newCategory.trim().length > 0;
    }
  },
  mounted() {
    this.fetchCategories();
  },
};
</scriPt>

<style scoped>
.form-container {
    padding: 20px;
    border-radius: 10px;
    font-family: "Wix Madefor Display", sans-serif;
    box-sizing: border-box;
}

.form-title {
    font-size: 32px;
    font-weight: bold;
    text-align: left;
    margin-bottom: 40px;
    color: white;
    font-family: "Wix Madefor Display", sans-serif;
}

.form-content {
    max-height: calc(80vh - 200px);
    padding: 10px;
    margin: 0;
    overflow-y: auto;
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
    width: 90%;
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
    margin-top: 60px;
    justify-content: space-between;
}

.cancel-button {
    background-color: #25262B;
    color: white;
    border-radius: 20px;
    border: 2px solid white;
    padding: 15px 35px;
    cursor: pointer;
    font-size: 16px;
    font-weight: bold;
    font-family: "Wix Madefor Display", sans-serif;
}

.submit-button {
    background-color: white;
    color: #25262B;
    border: none;
    padding: 13px 35px;
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
    margin-bottom: 20px;
    margin-bottom: 10px;
    font-family: "Wix Madefor Display", sans-serif;
}

.categories-select {
    padding: 15px 20px;
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
    margin-left: 8px;
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
    margin-top: 10px;
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
    right: 30px;
    top: 50%;
    transform: translateY(-30%);
    color: white;
    pointer-events: none;
}

.date-container input[type="date"]::-webkit-calendar-picker-indicator {
    opacity: 0;
    cursor: pointer;
}

.icons-wrapper {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 20px;
}

.selected-text {
    font-size: 20px;
    color: white;
}
.selected-icon {
    font-size: 36px;
    color: white;
}
</style>

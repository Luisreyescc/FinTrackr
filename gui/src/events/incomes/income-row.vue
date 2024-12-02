<template>
  <div class="income-row">
    <div class="income-icon">
      <font-awesome-icon :icon="['fas', 'circle-dollar-to-slot']" class="row-icon"/>
    </div>
    <div class="income-details">
      <h4>{{ formattedCategories }}</h4>
      <p class="income-description">{{ income.description }}</p>
      <span class="income-date">{{ formattedDate }}</span>
    </div>
    <div class="income-amount-section">
      <span class="income-amount">{{ formattedAmount }}</span>
      <div class="income-actions">
        <button class="edit-button" @click="startEdit">
          <font-awesome-icon :icon="['fas', 'pen-to-square']" class="icon" />
        </button>
        <button class="delete-button" @click="deleteIncome">
          <font-awesome-icon :icon="['fas', 'trash-can']" class="icon" />
        </button>
      </div>
    </div>
  </div>

  <div v-if="isEditing" class="overlay" @click="cancelEdit"></div>
  <div v-if="isEditing" class="edit-popup">
    <h3 class="edit-title">Edit Income</h3>
    <div class="popup-content">
      <form @submit.prevent="submitEdit">
        <label>
          Amount:
          <input
            type="text"
            v-model="editIncome.amount"
            @input="validateAmount"
            :class="{ 'input-error': amountError, 'input-valid': !amountError && editIncome.amount }"
            placeholder="Enter amount (e.g., 1000.00)"/>
        </label>
        <span v-if="amountError" class="error-message">{{ amountError }}</span>

        <div class="categories-wrapper">
          <div class="categories-select" @click="toggleDropdown">
            Sources
            <span class="dropdown-icon">
              <font-awesome-icon v-if="!dropdownOpen" :icon="['fas', 'angle-right']"/>
              <font-awesome-icon v-else :icon="['fas', 'angle-down']"/>
            </span>
          </div>

          <ul v-if="dropdownOpen" class="categories-dropdown scrollbar">
            <li v-if="loadingCategories">Loading categories...</li>
            <li v-else @click="showNewCategoryDialog" style="color: green; font-weight: bold" >
              <font-awesome-icon :icon="['fas', 'plus']" font-size="12" /> New source
            </li>
            <li
              v-for="(category, index) in categoryOptions"
              :key="index"
              @click="addCategory(category)">{{ category }}
            </li>
          </ul>

          <div v-if="showNewCategory" @click="cancelNewCategory"></div>
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
            <span v-for="(category, index) in income.categories" :key="index" class="tag">
              {{ category }}
              <button @click="removeCategory(index)" class="close-button">
                <font-awesome-icon :icon="['fas', 'xmark']" />
              </button>
            </span>
          </div>
        </div>

        <label>
          Description:
          <input
            type="text"
            v-model="editIncome.description"
            @input="validateTextField('description')"
            :class="{
              'input-error': descriptionError,
              'input-valid': !descriptionError
              && editIncome.description }"
            placeholder="Enter a description for the income"/>
        </label>
        <span v-if="descriptionError" class="error-message">{{ descriptionError }}</span>

        <label>
          Date:
          <input
            v-model="editIncome.date"
            type="date"
            @input="validateDate"
            :class="{ 'input-error': dateError, 'input-valid': !dateError && editIncome.date }"/>
        </label>
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
import "@/css/scrollbar.css";
import axios from "axios";

export default {
  name: "IncomeRow",
  props: {
    income: {
      type: Object,
      required: true,
      default: () => ({ categories: [] }),
    },
  },
  data() {
    return {
      isEditing: false,
      editIncome: {
        ...this.income,
        categories: this.income.categories || []
      },
      
      localIncome: { ...this.income }, //
      
      amountError: "",
      descriptionError: "",
      dateError: "",
      categoryOptions: [],
      dropdownOpen: false,
      showNewCategory: false,
      newCategory: "",
      loadingCategories: false,    };
  },
  computed: {
    formattedAmount() {
      // This for give the amount format in USD
      const formatter = new Intl.NumberFormat("en-US", {
        style: "currency",
        currency: "USD",
      });
      return `+ ${formatter.format(this.income.amount)}`;
    },
    formattedCategories() {
      return this.income.categories ? this.income.categories.join(", ") : "No categories";
    },
    formattedDate() {
      // Data format year-MONTH-day
      const date = new Date(this.income.date);
      const day = String(date.getDate()).padStart(2, "0");
      const month = date.toLocaleString("en-US", { month: "short" }).toUpperCase();
      const year = date.getFullYear();
      return `${year}-${month}-${day}`;
    },
    isSubmitEnabled() {
      return this.income.categories && this.income.categories.length > 0;
    },
    isAcceptEnabled() {
      return this.newCategory.trim().length > 0;
    },
  },
  methods: {
    startEdit() {
      this.isEditing = true;
      this.editIncome = {
        ...this.income,
        categories: [...this.income.categories],
      };
    },
    cancelEdit() {
      this.isEditing = false;
      this.editIncome = { ...this.income };
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
    submitEdit() { //async submitEdit() {}
      this.clearErrors();

      const isAmountValid = this.validateAmount();
      const isDescriptionValid = this.validateTextField("description");
      const isDateValid = this.validateDate();

      /* if (isAmountValid && isDescriptionValid && isDateValid) {
        this.editIncome.date = new Date(this.editIncome.date).toISOString().split("T")[0];

	const token = localStorage.getItem("token");
        if (!token) {
          console.error("No token found");
          return;
        }
        try {
          const response = await axios.put(
            `http://localhost:8000/api/incomes/${this.editIncome.income_id}/`,
            this.editIncome,
            {
              headers: { Authorization: `Bearer ${token}` },
            },
          );
          Object.assign(this.localIncome, response.data);
          this.$emit("updateIncome", { ...this.localIncome });
          this.isEditing = false;
        } catch (error) {
          console.error(
            "Error al actualizar el ingreso:",
            error.response?.data || error.message,
          );
        }
	} */
      if (isAmountValid && isDescriptionValid && isDateValid) {
        this.$emit("updateIncome", this.editIncomes);
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
        const response = await axios.get(
          "http://localhost:8000/api/income-categories/",
          {
            headers: { Authorization: `Bearer ${token}` },
          },
        );
        this.categoryOptions = response.data.categories || [];
      } catch (error) {
        console.error("Error fetching categories:", error);
      } finally {
        this.loadingCategories = false;
      }
    },
    addCategory(category) {
      if (!this.editIncome.categories.includes(category)) {
        this.editIncome.categories.push(category);
        this.newCategory = "";
      }
      this.dropdownOpen = false;
    },
    removeCategory(index) {
      this.localIncome.categories.splice(index, 1);
      this.$emit("updateIncome", { ...this.localIncome });
    },
    showNewCategoryDialog() {
      this.newCategory = "";
      this.showNewCategory = true;
    },
    cancelNewCategory() {
      this.showNewCategory = false;
    },
    validateAmount() {
      const amountPattern = /^\d{1,10}(\.\d{0,2})?$/;
      if (!this.editIncome.amount) {
        this.amountError = "Amount is required";
        return false;
      }
      if (!amountPattern.test(this.editIncome.amount)) {
        this.amountError = "Invalid amount format";
        return false;
      }
      return true;
    },
    validateTextField(field) {
      this[`${field}Error`] = "";
      if (!this.editIncome[field]) {
        this[`${field}Error`] = `${field.charAt(0).toUpperCase() + field.slice(1)} is required`;
        return false;
      }
      if (this.editIncome[field].length > 180) {
        this[`${field}Error`] = "Exceeded the maximum character limit of 180";
        return false;
      }
      return true;
    },
    validateDate() {
      if (!this.editIncome.date) {
        this.dateError = "Date is required";
        return false;
      }
      return true;
    },
    deleteIncome() {
      console.log("Removing income");
      this.$emit("deleteIncome", this.income.income_id);
    },
  },
  mounted() {
    this.fetchCategories();
  },
};
</script>

<style scoped>
.income-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 15px;
    background-color: #f9f9f9;
    border-radius: 8px;
    margin-bottom: 10px;
    box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1);
}

.income-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 80px;
    height: 80px;
    border-radius: 50%;
    background-color: #e0e0e0;
    margin-right: 14px;
}

.row-icon {
    font-size: 38px;
    color: #25253C;
}

.income-details {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    overflow: hidden;
}

.income-details h4, .income-description {
    margin: 0;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 440px;
    margin-left: 10px;
}

.income-details h4 {
    font-size: 22px;
    color: #21255b;
    font-weight: bold;
}

.income-description {
    color: #777;
    font-weight: bold;
    font-size: 20px;
}

.income-date {
    color: #aaa;
    font-weight: bold;
    font-size: 18px;
    margin-left: 10px;
    white-space: nowrap;
}

.income-amount-section {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    margin-left: 25px;
}

.income-amount {
    font-weight: bold;
    color: #4caf50;
    font-size: 20px;
    flex-shrink: 0;
}

.income-actions {
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
    background-color: #25253c;
    color: white;
}

.edit-button:hover {
    transform: scale(1.1);
    background-color: #555;
}

.delete-button {
    background-color: red;
    color: white;
}

.delete-button:hover {
    transform: scale(1.1);
    background-color: darkred;
}

.icon {
    font-size: 20px;
    color: white;
}

.edit-popup {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background-color: white;
    border-radius: 8px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
    padding: 20px;
    width: 400px;
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
    font-size: 22px;
    font-weight: bold;
    color: #333;
    text-align: left;
    margin-bottom: 40px;
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
    border-bottom-color: #1b1f9c;
    background-color: #e0f7fa;
    outline: none;
}

.error-message {
    color: red;
    font-size: 12px;
}

.button-group {
    display: flex;
    gap: 10px;
    justify-content: space-between;
    margin-top: 20px;
}

.cancel-button {
    background-color: #333;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 4px;
    cursor: pointer;
    font-family: "Wix Madefor Display", sans-serif;
}

.submit-button {
    background-color: #4caf50;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 4px;
    cursor: pointer;
    font-family: "Wix Madefor Display", sans-serif;
}

.cancel-button:hover {
    background-color: #555;
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
    transition:
	background-color 0.3s,
	color 0.3s;
    text-align: left;
}

.categories-dropdown li:hover {
    background-color: #f0f8ff;
    border-radius: 12px;
    color: #1010ac;
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
    background-color: #f3f3f9;
    border: 1px solid #6f6f7a;
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

.cancel-category,
.accept-category {
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
    background-color: #a2cbb2;
    cursor: not-allowed;
    opacity: 0.7;
}
</style>

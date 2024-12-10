<template>
  <div class="debt-row">
    <div class="debt-checkbox" :class="{ 'checked': debt.is_payed }" @click="markAsPaid">
      <font-awesome-icon v-if="debt.is_payed" :icon="['fas', 'check']" class="check-icon"/>
    </div>
    <div class="debt-details">
      <h4>{{ formattedCategories }}</h4>
      <p class="debt-description">{{ formattedDescription }}</p>
      <span class="debt-date">{{ formattedDate }}</span>
    </div>
    <div class="debt-amount-section">
      <span class="debt-amount">{{ formattedAmount }}</span>
      <div class="debt-actions">
        <button class="edit-button" @click="startEdit" :disabled="isChecked">
          <font-awesome-icon :icon="['fas', 'pen-to-square']" class="edit-icon"/>
        </button>
        <button class="delete-button" @click="deleteDebt">
          <font-awesome-icon :icon="['fas', 'trash-can']" class="trash-icon" />
        </button>
      </div>
    </div>
  </div>

  <div v-if="showConfirmPopup" class="overlay" @click="cancelConfirm"></div>
  <div v-if="showConfirmPopup" class="confirm-popup">
    <h3 class="warning-title">Warning</h3>
    <p>Marking a debt as paid is permanent and cannot be undone.</p>
  <p>Once marked as paid, you will no longer be able to edit it, but you can delete it.</p>
  <p>Are you sure you want to mark this debt as paid?</p>
    <div class="buttons-group">
      <button class="quit-button" @click="cancelConfirm">Cancel</button>
      <button class="confirm-button" @click="confirmMark">Confirm</button>
    </div>
  </div>

  <div v-if="isEditing" class="overlay" @click="cancelEdit"></div>
  <div v-if="isEditing" class="edit-popup">
    <h3 class="edit-title">Edit Debt</h3>
    <div class="popup-content scrollbar">
      <form @submit.prevent="submitEdit">
        <label>
          Amount:
          <input
            type="text"
            v-model="editDebt.amount"
            @input="validateAmount"
            :class="{ 'input-error': amountError, 'input-valid': !amountError && editDebt.amount }"
            placeholder="Enter amount (e.g., 1000.00)"/>
        </label>
        <span v-if="amountError" class="error-message">{{ amountError }}</span>

	<label>
          Creditor:
          <input
            type="text"
            v-model="editDebt.debtor_name"
            @input="validateTextField('debtor_name')"
            :class="{ 'input-error': creditorError, 'input-valid': !creditorError && editDebt.debtor_name }"
            placeholder="Enter the name of your creditor"/>
        </label>
        <span v-if="creditorError" class="error-message">{{ creditorError }}</span>
	
        <label>
          Description:
          <input
            type="text"
            v-model="editDebt.description"
            @input="validateTextField('description')"
            :class="{
                    'input-error': descriptionError,
                    'input-valid': !descriptionError && editDebt.description }"
            placeholder="Enter a description for the debt"/>
        </label>
        <span v-if="descriptionError" class="error-message">{{ descriptionError }}</span>

        <div class="categories-wrapper">
          <div class="categories-select" @click="toggleDropdown">
            Categories
            <span class="dropdown-icon">
              <font-awesome-icon v-if="!dropdownOpen" :icon="['fas', 'angle-right']"/>
              <font-awesome-icon v-else :icon="['fas', 'angle-down']" />
            </span>
          </div>

          <ul v-if="dropdownOpen" class="categories-dropdown scrollbar">
            <li v-if="loadingCategories">Loading categories...</li>
            <li v-else @click="showNewCategoryDialog" style="color: #BF9F00; font-weight: bold">
              <font-awesome-icon :icon="['fas', 'plus']" font-size="12" /> New category
            </li>
            <li
              v-for="(category, index) in categoryOptions"
              :key="index"
              @click="addCategory(category)">
              {{ category }}
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
            <span v-for="(category, index) in editDebt.categories" :key="index" class="tag">
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
          <font-awesome-icon class="birth-icon" :icon="['fas', 'calendar']" />
          <input
            v-model="editDebt.date"
            type="date"
            @input="validateDate"
            class="custom-date-input"
            :class="{
              'input-error': dateError,
              'input-valid': !dateError && editDebt.date }"/>
        </div>
        <span v-if="dateError" class="error-message">{{ dateError }}</span>

	<div class="icons-wrapper">
          <IconDropdown
            :iconOptions="iconOptions"
            :currentIcon="editDebt.icon"
            @iconSelected="applyIcon" />
          <span class="selected-text">Selected Icon: </span>
          <span v-if="editDebt.icon" class="selected-icon">
            <font-awesome-icon :icon="parseIcon(editDebt.icon)"/>
          </span>
        </div>
	
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
import IconDropdown from "@/components/icon-dropdown.vue";

export default {
  name: "DebtRow",
  components: {
    IconDropdown
  },
  props: {
    debt: {
      type: Object,
      required: true,
      default: () => ({ categories: [] }),
    },
  },
  data() {
    return {
      isEditing: false,
      editDebt: {
        ...this.debt,
        categories: this.debt.categories || [],
      },
      amountError: "",
      descriptionError: "",
      dateError: "",
      creditorError: "",
      categoryOptions: [],
      dropdownOpen: false,
      showNewCategory: false,
      newCategory: "",
      loadingCategories: false,
      isChecked: this.debt.isChecked || false,
      showConfirmPopup: false,
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
  computed: {
    formattedAmount() {
      const formatter = new Intl.NumberFormat("en-US", {
        style: "currency",
        currency: "USD",
      });
      return `${formatter.format(this.debt.amount)}`;
    },
    formattedCategories() {
      return this.debt.categories
        ? this.debt.categories.join(", ")
        : "No categories";
    },
    formattedDate() {
      const date = new Date(this.debt.date);
      const day = String(date.getDate()).padStart(2, "0");
      const month = date.toLocaleString("en-US", { month: "short" }).toUpperCase();
      const year = date.getFullYear();
      return `${year}-${month}-${day}`;
    },
    formattedDescription() {
      const creditor = this.debt.debtor_name || "No Creditor";
      const description = this.debt.description || "No Description ";
      return `${creditor}: ${description}`;
    },
    isSubmitEnabled() {
      return this.editDebt.categories && this.editDebt.categories.length > 0 && this.editDebt.icon;
    },
    isAcceptEnabled() {
      return this.newCategory.trim().length > 0;
    },
  },
  methods: {
    cancelConfirm() {
      this.showConfirmPopup = false;
    },
    confirmMark() {
      this.isChecked = true;
      this.showConfirmPopup = false;
      this.$emit("markDebtAsPaid", {
        ...this.debt,
        isChecked: true,
      });
    },
    triggerConfirmation() {
      if (!this.isChecked) {
        this.showConfirmPopup = true;
      }
    },
    markAsPaid() {
      if (this.debt.is_payed) return;
      this.showConfirmPopup = true;
    },
    startEdit() {
      if (this.isChecked)
	return;
      this.isEditing = true;
      this.editDebt = {
        ...this.debt,
        categories: [...this.debt.categories],
        date: this.formatDateForInput(this.debt.date),
      };
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
      this.creditorError = "";
    },
    toggleDropdown() {
      this.dropdownOpen = !this.dropdownOpen;
    },
    parseIcon(iconString) {
      if (typeof iconString === 'string') {
        return iconString.split(' ');
      }
      return iconString;
    },
    submitEdit() {
      this.clearErrors();

      const isAmountValid = this.validateAmount();
      const isDescriptionValid = this.validateTextField("description");
      const isDateValid = this.validateDate();
      const isCreditorValid = this.validateTextField("debtor_name");

      if (isAmountValid && isDescriptionValid && isDateValid && isCreditorValid) {
        const iconString = Array.isArray(this.editDebt.icon) ? this.editDebt.icon.join(' ') : this.editDebt.icon;
        const debtData = {
          ...this.editDebt,
          icon: iconString,
        };

        this.$emit('updateDebt', debtData);
        this.isEditing = false;
        this.fetchCategories();
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
          "http://localhost:8000/api/debt-categories/",
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
    acceptNewCategory() {
      if (this.newCategory.trim()) {
        const newCategory = this.newCategory.trim();
        if (!this.categoryOptions.includes(newCategory)) {
          this.categoryOptions.push(newCategory);
        }
        if (!this.editDebt.categories.includes(newCategory)) {
          this.editDebt.categories.push(newCategory);
        }
        this.newCategory = "";
        this.showNewCategory = false;
        this.dropdownOpen = false;
      }
    },
    addCategory(category) {
      if (!this.editDebt.categories.includes(category)) {
        this.editDebt.categories.push(category);
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
    removeCategory(index, event) {
      event.stopPropagation();
      event.preventDefault();
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
        this[`${field}Error`] =
          `${field.charAt(0).toUpperCase() + field.slice(1)} is required`;
        return false;
      }
      if (this.editDebt[field].length > 120 && field === "creditor") {
        this[`${field}Error`] = "Exceeded the maximum character limit of 120";
        return false;
      }
      if (this.editDebt[field].length > 120 && field === "description") {
        this[`${field}Error`] = "Exceeded the maximum character limit of 120";
        return false;
      }
      return true;
    },
    validateDate() {
      if (!this.editDebt.date) {
        this.dateError = "Date is required";
        return false;
      }
      return true;
    },
    deleteDebt() {
      console.log("Removing debt");
      this.$emit("deleteDebt", this.debt.debt_id);
    },
    formatDateForInput(date) {
      const d = new Date(date);
      const month = String(d.getMonth() + 1).padStart(2, "0");
      const day = String(d.getDate()).padStart(2, "0");
      const year = d.getFullYear();
      return `${year}-${month}-${day}`;
    },
    applyIcon(selectedIcon) {
      this.editDebt.icon = selectedIcon;
    },
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
    background: #25262b;
    border: 2px solid white;
    border-radius: 20px;
    margin-bottom: 10px;
    box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1);
}

.debt-checkbox {
    width: 40px;
    height: 40px;
    border: 2px solid white;
    border-radius: 5px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    background-color: transparent;
    transition: background-color 0.3s, border-color 0.3s;
    margin-left: 5px;
}

.debt-checkbox.checked {
    border-color: #4DBEC8;
    background: #4DBEC8;
}

.check-icon {
    color: white;
    font-size: 36px;
}


.debt-details {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    overflow: hidden;
    margin-left: 10px;
}

.debt-details h4,
.debt-description {
    margin: 0;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 420px;
    margin-left: 10px;
}

.debt-details h4 {
    font-size: 22px;
    color: #6092de;
    font-weight: bold;
}

.debt-description {
    color: white;
    font-weight: bold;
    font-size: 20px;
}

.debt-date {
    color: #bf9f00;
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
}

.debt-amount {
    font-weight: bold;
    color: #6092de;
    font-size: 20px;
    flex-shrink: 0;
}

.debt-actions {
    display: flex;
    gap: 10px;
    margin-top: 5px;
}

.edit-button,
.delete-button {
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
    background-color: #f2f2f2;
}

.delete-button {
    background-color: #d55c5c;
    color: white;
}

.delete-button:hover {
    transform: scale(1.1);
    background-color: darkred;
}

.edit-icon {
    font-size: 20px;
    color: #25262b;
}

.trash-icon {
    font-size: 20px;
    color: white;
}

.edit-popup {
    max-height: calc(80vh - 200px);
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background: #25262b;
    border-radius: 12px;
    box-shadow: 0 4px 10px rgba(255, 255, 255, 0.1);
    padding: 20px;
    width: 600px;
    height: 730px;
    overflow: hidden; 
    z-index: 1000;
}

.popup-content {
    display: flex;
    flex-direction: column;
    height: 680px;
    overflow-y: auto;
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
    background-color: #25262b;
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
    border-color: #d55c5c;
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
    color: #d55c5c;
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
    background-color: #25262b;
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
    color: #25262b;
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
    color: #25262b;
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
    color: #25262b;
}

.categories-dropdown {
    position: absolute;
    top: 80%;
    left: 0;
    right: 0;
    border: 1px solid #3f4049;
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
    transition:	background-color 0.3s, color 0.3s;
    text-align: left;
    color: white;
    font-weight: bold;
}

.categories-dropdown li:hover {
    background-color: white;
    border-radius: 12px;
    color: #25262b;
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
    color: #25262b;
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
    color: #25262b;
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
    color: #25262b;
    font-family: "Wix Madefor Display", sans-serif;
}

.new-category-dialog input {
    width: 90%;
    padding: 14px;
    margin-bottom: 2px;
    border: none;
    outline: none;
    color: #25262b;
    font-size: 18px;
    background-color: white;
    border-radius: 4px;
    border: 2px solid #25262b;
    transition:	background-color 0.3s,border-color 0.3s;
    font-family: "Wix Madefor Display", sans-serif;
}

.new-category-dialog input::placeholder {
    color: #25262b;
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
    background-color: #25262b;
    color: white;
}

.accept-category {
    background-color: white;
    color: #25262b;
    border: 2px solid #25262b;
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
    right: 26px;
    top: 50%;
    transform: translateY(-30%);
    color: white;
    pointer-events: none;
}

.date-container input[type="date"]::-webkit-calendar-picker-indicator {
    opacity: 0;
    cursor: pointer;
}

.confirm-popup {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background: #25262b;
    border-radius: 12px;
    padding: 20px;
    width: 650px;
    z-index: 1100;
    box-shadow: 0 4px 8px rgba(255, 255, 255, 0.2);
}

.warning-title {
    font-size: 32px;
    font-weight: bold;
    margin-bottom: 10px;
    text-align: center;
    color: white;
}

.confirm-popup p {
    display: block;
    margin-bottom: 10px;
    font-weight: bold;
    font-size: 24px;
    color: white;
    font-family: "Wix Madefor Display", sans-serif;
}

.buttons-group {
    display: flex;
    justify-content: space-between;
}

.quit-button, .confirm-button {
    padding: 15px 30px;
    margin-top: 30px;
    border: none;
    border-radius: 3px;
    cursor: pointer;
    font-size: 16px;
    font-weight: bold;
    font-family: "Wix Madefor Display", sans-serif;
}

.quit-button {
    background-color: #25262B;
    color: white;
    border: 2px solid white;
}

.confirm-button {
    background-color: white;
    color: #25262B;
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

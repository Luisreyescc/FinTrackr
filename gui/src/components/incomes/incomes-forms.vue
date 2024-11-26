<template>
<div class="form-container" >
  <h3 class="form-title">New Income Data</h3>
  <div class="form-content scrollbar">
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
    
    <div class="sources-wrapper">
      <div class="sources-select" @click="toggleDropdown">
	Sources
	<span class="dropdown-icon">
	<font-awesome-icon v-if="!dropdownOpen" :icon="['fas', 'angle-right']" />
	<font-awesome-icon v-else :icon="['fas', 'angle-down']" />
	</span>
      </div>

      <ul v-if="dropdownOpen" class="sources-dropdown scrollbar">
	<li v-if="loadingSources">Loading sources...</li>
	<li v-else @click="showNewSourceDialog" style="color: green; font-weight: bold;">
          <font-awesome-icon :icon="['fas', 'plus']" font-size="12" /> New source
	</li>
        <li
          v-for="(source, index) in sourceOptions"
          :key="index"
          @click="newSource(source)">{{ source }}
	</li>
      </ul>

      <div v-if="showNewSource" class="overlay" @click="cancelNewSource"></div>
      <div v-if="showNewSource" class="new-source-dialog">
	<h4>Enter new source</h4>
	<input
          type="text"
          v-model="newSource"
          placeholder="New source"
          :maxlength="18" />
	<div class="button-group">
          <button @click="cancelNewSource" class="cancel-source">Cancel</button>
          <button
            @click="acceptNewSource"
            class="accept-source"
            :disabled="!isAcceptEnabled">Accept</button>
	</div>
      </div>
      
      <div class="selected-sources">
        <span v-for="(source, index) in income.sources" :key="index" class="tag">
          {{ source }}
          <button @click="removeSource(index)" class="close-button">
            <font-awesome-icon :icon="['fas', 'xmark']"/>
          </button>
        </span>
      </div>
    </div>
    
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
      <button type="submit" class="submit-button" :disabled="!isSubmitEnabled">Submit</button>
      </div>
  </form>
  </div>
</div>
</template>

<script>
import '@/css/scrollbar.css';
import axios from 'axios';
  
export default {
  name: "IncomesForm",
  data() {
    return {
      income: { amount: '', sources: [], description: '', date: '' },
      amountError: "",
      descriptionError: "",
      dateError: "",
      sourceOptions: [],
      dropdownOpen: false,
      showNewSource: false,
      newSource: "",
      loadingSources: false,
    };
  },
  methods: {
    submitForm() {
      this.clearErrors();

      const isAmountValid = this.validateAmount();
      const isDescriptionValid = this.validateTextField('description');
      const isDateValid = this.validateDate();
      
      if (isAmountValid && isDescriptionValid && isDateValid) {
	this.$emit('submitForm', { ...this.income });
	this.$emit('closeForm');
	this.resetForm();
      }
    },
    toggleDropdown() {
      this.dropdownOpen = !this.dropdownOpen;
    },
    async fetchSources() {
      try {
        this.loadingSources = true;
        const response = await axios.get('/api/sources-backend-url');
        this.sourceOptions = response.data; // Asuming backend returns an array of categories
      } catch (error) {
        console.error("Error fetching sources:", error);
      } finally {
        this.loadingSources = false;
      }
    },
    async sendNewSource() {
      try {
        const response = await axios.post('/api/sources', { name: this.newSource.trim() });
        if (response.status === 201) {
          // Add new category to the user's categories table if the backend respons with success
          this.sourceOptions.push(this.newSource.trim());
          this.income.sources.push(this.newSource.trim());
        } else {
          console.error("Failed to add source:", response.statusText);
        }
      } catch (error) {
        console.error("Error adding new source:", error);
      }
    },
    addSource(source) {
      if (!this.income.sources.includes(source)) {
        this.income.sources.push(source);
      }
      this.dropdownOpen = false;
    },
    showNewSourceDialog() {
      this.newSource = "";
      this.showNewSource = true;
    },
    cancelNewSource() {
      this.showNewSource = false;
    },
    async acceptNewSource() {
      if (this.newSource.trim()) {
        await this.sendNewSource();
        this.income.source.push(this.newSource);
        this.showNewSource = false;
        this.newSource = "";
	this.dropdownOpen = false;
      }
    },
    removeSource(index) {
      this.income.sources.splice(index, 1);
    },
    clearErrors() {
      this.amountError = "";
      this.descriptionError = "";
      this.dateError = "";
    },
    cancelForm() {
      this.resetForm();
      this.$emit('closeForm');
    },
    resetForm() {
      this.income = { amount: '', source: [], description: '', date: '' };
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
  },
  computed: {
    isSubmitEnabled() {
      return this.income.sources.length > 0;
    },
    isAcceptEnabled() {
      return this.newSource.trim().length > 0;
    },
  },
  mounted() {
    this.fetchSources();
  },
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
    scrollbar-width: thin;
    scrollbar-color: #1B1F9C #e0e0e0;
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

.sources-wrapper {
    position: relative;
    margin-bottom: 20px;
    font-family: "Wix Madefor Display", sans-serif;
}

.sources-select {
    padding: 12px 15px;
    border: 1px solid #ccc;
    border-radius: 8px;
    cursor: pointer;
    display: flex;
    align-items: center;
    width: 85px;
    font-weight: bold;
    background-color: #ffffff;
    box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1);
    transition: background-color 0.2s;
}

.sources-select:hover {
    background-color: #f8f9fa;
}

.dropdown-icon {
    width: 16px;
    height: 16px;
    margin-left: 8px;
    transform: translateY(-1px);
    color: #21255b;
}

.sources-dropdown {
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

.sources-dropdown li {
    padding: 10px 20px;
    cursor: pointer;
    transition: background-color 0.3s, color 0.3s;
    text-align: left;
}

.sources-dropdown li:hover {
    background-color: #f0f8ff;
    border-radius: 12px;
    color: #1010AC;
    font-weight: bold;
}

.selected-sources {
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

.new-source-dialog {
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

.new-source-dialog h4 {
  margin: 0 0 10px;
  font-size: 18px;
  color: #21255b;
  font-family: "Wix Madefor Display", sans-serif;
}

.new-source-dialog input {
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

.new-source-dialog .button-group {
    display: flex;
    justify-content: space-between;
    margin-top: 15px;
}

.cancel-source, .accept-source {
    color: white;
    border: none;
    padding: 8px 18px;
    border-radius: 2px;
    cursor: pointer;
    font-size: 14px;
    font-weight: bold;
    font-family: "Wix Madefor Display", sans-serif;
}

.cancel-source {
    background-color: #333; 
}

.accept-source {
    background-color: #4caf50; 
}

.cancel-button:hover {
    background-color: #616161;
}

.submit-button:hover {
    background-color: #237242;
}

.submit-button:disabled,
.accept-source:disabled {
    background-color: #A2CBB2;
    cursor: not-allowed;
    opacity: 0.7;
}
</style>

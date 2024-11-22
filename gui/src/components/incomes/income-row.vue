<template>
  <div class="income-row">
    <div class="income-icon">
       <font-awesome-icon :icon="['fas', 'circle-dollar-to-slot']" font-size="28" color="#25253C"/>
    </div>
    <div class="income-details" >
      <h4>{{ income.source }}</h4>
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
	<font-awesome-icon :icon="['fas', 'trash-can']" class="icon"/>
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
          <input type="text"
            v-model="editIncome.amount"
            @input="validateAmount"
            :class="{ 'input-error': amountError, 'input-valid': !amountError && editIncome.amount }"
            placeholder="Enter amount (e.g., 1000.00)" />
        </label>
        <span v-if="amountError" class="error-message">{{ amountError }}</span>
        
        <label>
          Source:
          <input type="text"
            v-model="editIncome.source"
            @input="validateTextField('source')"
            :class="{ 'input-error': sourceError, 'input-valid': !sourceError && editIncome.source }"
            placeholder="Enter the source of the income" />
        </label>
          <span v-if="sourceError" class="error-message">{{ sourceError }}</span>

          <label>
            Description:
            <input type="text"
              v-model="editIncome.description"
              @input="validateTextField('description')"
              :class="{ 'input-error': descriptionError, 'input-valid': !descriptionError && editIncome.description }"
              placeholder="Enter a description for the income" />
          </label>
          <span v-if="descriptionError" class="error-message">{{ descriptionError }}</span>

          <label>
            Date:
            <input
              v-model="editIncome.date"
              type="date"
              @input="validateDate"
              :class="{ 'input-error': dateError, 'input-valid': !dateError && editIncome.date }" />
          </label>
          <span v-if="dateError" class="error-message">{{ dateError }}</span>

          <div class="button-group">
          <button type="button" class="cancel-button" @click="cancelEdit">Cancel</button><button type="submit" class="submit-button">Save</button>
          </div>
        </form>
      </div>
    </div>
</template>

<script>
export default {
  name: "IncomeRow",
  props: {
    income: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      isEditing: false,
      editIncome: { ...this.income },
      amountError: "",
      sourceError: "",
      descriptionError: "",
      dateError: "",
    };
  },
  computed: {
    formattedAmount() {
      // This for give the amount format in USD
      const formatter = new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
      });
      return `+ ${formatter.format(this.income.amount)}`;
    },
    formattedDate() {
      // Data format day-MONTH-year
      const date = new Date(this.income.date);
      const day = String(date.getDate()).padStart(2, '0');
      const month = date.toLocaleString('en-US', { month: 'short' }).toUpperCase();
      const year = date.getFullYear();
      return `${day}-${month}-${year}`;
    }
  },
  methods: {
    startEdit() {
      this.isEditing = true;
      this.editIncome = { ...this.income };
    },
    cancelEdit() {
      this.isEditing = false;
      this.editIncome = { ...this.income };
      this.clearErrors();
    },
    submitEdit() {
      this.clearErrors();

      const isAmountValid = this.validateAmount();
      const isSourceValid = this.validateTextField("source");
      const isDescriptionValid = this.validateTextField("description");
      const isDateValid = this.validateDate();

      if (isAmountValid && isSourceValid && isDescriptionValid && isDateValid) {
        this.$emit("updateIncome", this.editIncome);
        this.isEditing = false;
      }
    },
    clearErrors() {
      this.amountError = "";
      this.sourceError = "";
      this.descriptionError = "";
      this.dateError = "";
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
      console.log(this.income.income_id);
      this.$emit("deleteIncome", this.income.income_id);
    }
  }
};
</script>

<style scoped>
.income-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 15px;
    background-color: #F9F9F9;
    border-radius: 8px;
    margin-bottom: 10px;
    box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1);
}

.income-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 60px;
    height: 60px;
    border-radius: 50%;
    background-color: #e0e0e0;
    margin-right: 14px;
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
    font-size: 16px;
    color: #21255b;
    font-weight: bold;
}

.income-description {
    color: #777;
    font-weight: bold;
    font-size: 14px;
}

.income-date {
    color: #aaa;
    font-weight: bold;
    font-size: 12px;
    margin-left: 10px;
    white-space: nowrap;
}

.income-amount-section {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    margin-left: 15px;
}

.income-amount {
    font-weight: bold;
    color: #4CAF50;
    font-size: 16px;
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
    width: 32px;
    height: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
    border: none;
    transition: transform 0.2s, background-color 0.2s;
}

.edit-button {
    background-color: #25253C;
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
    font-size: 16px;
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
    border-bottom-color: #1B1F9C;
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
</style>

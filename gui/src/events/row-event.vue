<template>
  <div :class="rowClass">
    <div v-if="incomes" v-else="expenses" class="event-icon">
      <font-awesome-icon :icon="icon" :style="{ fontSize: '28px', color: '#25253C' }" />
    </div>
    <div v-else="debts" class="debts-ckeck">
    <div class="event-details">
      <h4>{{ formattedCategories }}</h4>
      <p class="event-description">{{ event.description }}</p>
      <span class="event-date">{{ formattedDate }}</span>
    </div>
    <div class="event-amount-section">
      <span :class="amountClass">{{ formattedAmount }}</span>
      <div class="event-actions">
        <button class="edit-button" @click="startEdit">
          <font-awesome-icon :icon="['fas', 'pen-to-square']" class="icon" />
        </button>
        <button class="delete-button" @click="deleteEvent">
          <font-awesome-icon :icon="['fas', 'trash-can']" class="icon" />
        </button>
      </div>
    </div>
    <v-if="incomes" EditIncomes
      v-if="isEditing"
      :event="event"
      :type="currentType"
      @closeEdit="cancelEdit"
      @updateEvent="submitEdit"/>
  </div>
</template>

<script>
import EditRow from '@/components/edit-row.vue';

export default {
  name: 'EventRow',
  components: {
    EditRow
  },
  props: {
    event: {
      type: Object,
      required: true,
    },
    type: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      isEditing: false,
    };
  },
  computed: {
    rowClass() {
      return this.type === 'income' ? 'income-row' : 'expense-row';
    },
    icon() {
      return this.type === 'income'
        ? ['fas', 'circle-dollar-to-slot']
        : ['fas', 'money-bill-transfer'];
    },
    amountClass() {
      return this.type === 'income' ? 'income-amount' : 'expense-amount';
    },
    formattedAmount() {
      const sign = this.type === 'income' ? '+' : '-';
      const formatter = new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
      });
      return ${sign} ${formatter.format(this.event.amount)};
    },
    formattedCategories() {
      return this.event.categories ? this.event.categories.join(', ') : 'No categories';
    },
    formattedDate() {
      const date = new Date(this.event.date);
      const day = String(date.getDate()).padStart(2, '0');
      const month = date.toLocaleString('en-US', { month: 'short' }).toUpperCase();
      const year = date.getFullYear();
      return ${year}-${month}-${day};
    },
  },
  methods: {
    startEdit() {
      this.isEditing = true;
    },
    cancelEdit() {
      this.isEditing = false;
    },
    submitEdit(updatedEvent) {
      this.$emit('updateEvent', updatedEvent);
      this.isEditing = false;
    },
    deleteEvent() {
      this.$emit('deleteEvent', this.event.id);
    },
  },
};
</script>

<style scoped>
.income-row, .expense-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 15px;
    background-color: #f9f9f9;
    border-radius: 8px;
    margin-bottom: 10px;
    box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1);
}

.event-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 60px;
    height: 60px;
    border-radius: 50%;
    background-color: #e0e0e0;
    margin-right: 14px;
}

.event-details {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    overflow: hidden;
}

.event-details h4 {
    font-size: 16px;
    color: #21255b;
    font-weight: bold;
}

.event-description {
    color: #777;
    font-weight: bold;
    font-size: 14px;
}

.event-date {
    color: #aaa;
    font-size: 12px;
}

.event-amount-section {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
}

.income-amount {
    color: #4caf50;
}

.expense-amount {
    color: #e42121;
}

.event-actions {
    display: flex;
    gap: 10px;
    margin-top 5px:
}

.edit-button,
.delete-button {
    border-radius: 10px;
    cursor: pointer;
    width: 32px;
    height: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
    border: none;
    transition:
	transform 0.2s,
	background-color 0.2s;
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
    font-size: 16px;
    color: white;
}
</style>

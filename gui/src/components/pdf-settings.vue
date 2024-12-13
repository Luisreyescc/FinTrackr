<template>
<div class="modal-overlay" @click="closeModal">
  <div class="modal-content" @click.stop>
    <h1>PDF Report Settings</h1>
    <button @click="closeModal" class="modal-close-icon">
      <font-awesome-icon :icon="['fas', 'xmark']"/>
    </button>
    
    <div class="section">
      <h2>Set Time</h2>
      <div class="time-selector">
        <div class="time-unit">
          <button @click="incrementTime('hour')" class="arrow-button">
            <font-awesome-icon :icon="['fas', 'angle-up']" class="arrow-icon"/>
          </button>
          <div class="time-value-container">
            <span class="time-value">{{ formatNumber(time.hour) }}</span>
          </div>
          <button @click="decrementTime('hour')" class="arrow-button">
            <font-awesome-icon :icon="['fas', 'angle-down']" class="arrow-icon"/>
          </button>
        </div>
        <span class="chars">:</span>
        <div class="time-unit">
          <button @click="incrementTime('minute')" class="arrow-button">
            <font-awesome-icon :icon="['fas', 'angle-up']" class="arrow-icon"/>
          </button>
          <div class="time-value-container">
            <span class="time-value">{{ formatNumber(time.minute) }}</span>
          </div>
          <button @click="decrementTime('minute')" class="arrow-button">
            <font-awesome-icon :icon="['fas', 'angle-down']" class="arrow-icon"/>
          </button>
        </div>
        <div class="time-unit">
          <button @click="toggleAmPm" class="time-button">{{ time.amPm }}</button>
        </div>
      </div>
    </div>
    
    <div class="section">
      <h2>Set Period</h2>
      <div class="period-selector">
        <div class="time-unit">
          <button @click="incrementPeriod('type')" class="arrow-button">
            <font-awesome-icon :icon="['fas', 'angle-up']" class="arrow-icon"/>
          </button>
          <div class="time-value-container">
            <span class="time-value">{{ period.type }}</span>
          </div>
          <button @click="decrementPeriod('type')" class="arrow-button">
            <font-awesome-icon :icon="['fas', 'angle-down']" class="arrow-icon"/>
          </button>
        </div>
        <span class="chars">-</span>
        <div class="time-unit">
          <button @click="incrementPeriod('day')" class="arrow-button">
            <font-awesome-icon :icon="['fas', 'angle-up']" class="arrow-icon"/>
          </button>
          <div class="time-value-container">
            <span class="time-value">{{ period.day }}</span>
          </div>
          <button @click="decrementPeriod('day')" class="arrow-button">
            <font-awesome-icon :icon="['fas', 'angle-down']" class="arrow-icon"/>
          </button>
        </div>
      </div>
    </div>
    
    <button @click="confirmSettings" class="confirm-button">Set</button>
  </div>
</div>
</template>

<script>
import axios from "axios";
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';

export default {
  name: "PDFSettings",
  components: {
    FontAwesomeIcon
  },
  props: {
    isVisible: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      time: {
        hour: 3,
        minute: 0,
        amPm: 'AM'
      },
      period: {
        type: 'Monthly',
        day: 1
      },
      periodTypes: ['Monthly', 'Bimester', 'Trimester'],
    };
  },
  methods: {
    formatNumber(value) {
      return value.toString().padStart(2, '0');
    },
    incrementTime(field) {
      if (field === 'hour')
        this.time.hour = this.time.hour < 12 ? this.time.hour + 1 : 1;
      else if (field === 'minute')
        this.time.minute = this.time.minute < 59 ? this.time.minute + 1 : 0;
    },
    decrementTime(field) {
      if (field === 'hour')
        this.time.hour = this.time.hour > 1 ? this.time.hour - 1 : 12;
      else if (field === 'minute')
        this.time.minute = this.time.minute > 0 ? this.time.minute - 1 : 59;
    },
    toggleAmPm() {
      this.time.amPm = this.time.amPm === 'AM' ? 'PM' : 'AM';
    },
    incrementPeriod(field) {
      if (field === 'type') {
        const currentIndex = this.periodTypes.indexOf(this.period.type);
        this.period.type = this.periodTypes[(currentIndex + 1) % this.periodTypes.length];
      } else if (field === 'day') {
        const maxDay = this.getMaxDay();
        this.period.day = this.period.day < maxDay ? this.period.day + 1 : 1;
      }
    },
    decrementPeriod(field) {
      if (field === 'type') {
        const currentIndex = this.periodTypes.indexOf(this.period.type);
        this.period.type =
          this.periodTypes[(currentIndex - 1 + this.periodTypes.length) % this.periodTypes.length];
      } else if (field === 'day') {
        const maxDay = this.getMaxDay();
        this.period.day = this.period.day > 1 ? this.period.day - 1 : maxDay;
      }
    },
    getMaxDay() {
      const today = new Date();
      const currentMonth = today.getMonth();
      const year = today.getFullYear();
      return new Date(year, currentMonth + 1, 0).getDate();
    },
    async confirmSettings() {
      const maxDay = this.getMaxDay();
      if (this.period.day > maxDay)
        this.period.day = maxDay;

      const token = localStorage.getItem("token");
      if (!token)
        return console.error("No token found");
      
      var interval = 1;
      if(this.period.type == "Bimester")
        interval = 2;
      else if(this.period.type == "Trimester")
        interval = 3;
      
      var hour = this.time.hour
      if(this.time.amPm == "PM" && hour!=12)
        hour+=12;
      else if(this.time.amPm == "AM" && hour == 12)
        hour=0;
      
      await axios.get(`http://localhost:8000/api/pdf/?action=start&interval=${interval}&day=${this.period.day}&hour=${hour}&minute=${this.time.minute}`, { headers: { Authorization: `Bearer ${token}` } });
      this.$emit('closeModal');
    },
    closeModal() {
      this.$emit('closeModal');
    },
  }
};
</script>

<style scoped>
.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1100;
}

.modal-content {
    background: #25262B;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 4px 10px rgba(255, 255, 255, 0.2);
    width: 500px;
    position: relative; 
}

.modal-content h1{
    color: white;
}

.modal-close-icon {
    position: absolute;
    top: 15px;
    right: 18px;
    background: none;
    border: none;
    font-size: 30px;
    color: white;
    cursor: pointer;
}

.section {
    margin: 20px 10px;
    color: white;
}

.time-selector, .period-selector {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 10px;
}

.time-unit {
    display: flex;
    flex-direction: column;
    align-items: center;
}

.arrow-button {
    font-size: 18px;
    background: none;
    border: none;
    cursor: pointer;
}

.arrow-icon {
    font-size: 28px;
    color: white;
}

.time-button {
    margin-left: 20px;
    padding: 10px 20px;
    background: white;
    border: none;
    border-radius: 3px;
    color: #25262B;
    cursor: pointer;
    font-size: 16px;
    font-weight: bold;
    font-family: "Wix Madefor Display", sans-serif;
}

.period-button:hover {
    background:  #3B3B5A;
}

.time-value-container {
    margin-top: 15px;
    margin-bottom: 15px;
    display: flex;
    flex-direction: column;
    align-items: center;
    position: relative;
}

.time-value, .chars {
    font-size: 24px;
    font-weight: bold;
    margin: 5px 0;
}

.time-value-container::before,
.time-value-container::after {
    content: '';
    position: absolute;
    width: 150%;
    height: 4px;
    background-color: #4E60D7;
    border-radius: 2px;
}

.time-value-container::before {
    top: -4px;
}

.time-value-container::after {
    bottom: -4px;
}

.confirm-button {
    margin-top: 15px;
    margin-bottom: 10px;
    padding: 15px 60px;
    background-color: #25262B;
    border: 2px solid white;
    border-radius: 3px;
    color: white;
    cursor: pointer;
    font-size: 20px;
    font-weight: bold;
    font-family: "Wix Madefor Display", sans-serif;
}

.confirm-button:hover {
    opacity: 0.8;;
}
</style>

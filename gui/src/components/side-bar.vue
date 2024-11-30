<template>
<div>
  <div v-if="isVisible" class="overlay" @click="$emit('closeSidebar')"></div>
  <div class="side-bar" :class="{ 'side-bar--visible': isVisible }">
    <button @click="$emit('closeSidebar')" class="close-button">
      <font-awesome-icon :icon="['fas', 'xmark']" class="close-button"/>
    </button>
    
    <div class="sidebar-logo">
      <font-awesome-icon :icon="['fab', 'docker']" class="logo-icon"/>
      <img src="@/assets/title.svg" alt="Logo" class="logo">
    </div>  
    
    <div class="divider_top"></div>
    
    <div v-if="currentPage === 'Home'" class="menu-options">
      <button @click="selectOption('Incomes')" class="menu-option">
	<font-awesome-icon :icon="['fas', 'chart-line']" class="icon"/> Incomes</button>
      <button @click="selectOption('Expenses')" class="menu-option">
	<font-awesome-icon :icon="['fas', 'money-bill-transfer']" class="icon"/> Expenses</button>
      <button @click="selectOption('Debts')" class="menu-option">
	<font-awesome-icon :icon="['fas', 'credit-card']" class="icon"/> Debts</button>
    </div>

    <div v-if="currentPage === 'Status'" class="menu-options">
      <button @click="selectOption('Account')" class="menu-option">
	<font-awesome-icon :icon="['fas', 'chart-area']" class="icon a"/>Account Status</button>
      <button @click="selectOption('Categories')" class="menu-option">
	<font-awesome-icon :icon="['fas', 'chart-pie']" class="icon a"/>Pie Charts</button>
    </div>
    
    <div class="divider_bottom"></div>
    
    <div class="bottom-options">
      <button @click="editProfile" class="bottom-option">
	<font-awesome-icon :icon="['fas', 'pen-to-square']" class="icon"/> Edit Profile</button>
      <button @click="pdfMail" class="bottom-option">
	<font-awesome-icon :icon="['fas', 'envelope-open-text']" class="icon"/> PDF Report</button>
      <button @click="logout" class="bottom-option">
        <font-awesome-icon :icon="['fas', 'right-from-bracket']" class="icon"/> Log-out</button>
    </div>
  </div>

  <div v-if="showPdfModal" class="modal-overlay" @click="closePdfModal">
    <div class="modal-content" @click.stop>
      <h1>PDF Report Settings</h1>
      <button @click="closePdfModal" class="modal-close-icon">
        <font-awesome-icon :icon="['fas', 'xmark']"/>
      </button>

      <div class="section">
	<h2>Set Time</h2>
	<div class="time-selector">
          <div class="time-unit">
            <button @click="incrementTime('hour')" class="arrow-button">
              <font-awesome-icon :icon="['fas', 'angle-up']" class="arrow-icon" />
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
</div>
</template>

<script>
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';

export default {
  name: "SideBar",
  components: {
    FontAwesomeIcon,
  },
  props: {
    isVisible: {
      type: Boolean,
      default: false
    },
    currentPage: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      showPdfModal: false,
      time: {
        hour: 3,
        minute: 0,
        amPm: 'AM'
      },
      period: {
        type: 'Month',
        day: 1
      },
      periodTypes: ['Monthly', 'Bimester', 'Trimester'],
    };
  },
  methods: {
    selectOption(option) {
      this.$emit('selectContent', option);
    },
    editProfile() {
      this.$router.push('/edit-profile');
    },
    logout() {
      sessionStorage.removeItem("isLoggedIn");
      localStorage.removeItem("token");
      this.$router.push("/");
    },
    pdfMail() {
      this.showPdfModal = true;
      this.$emit("closeSidebar");
    },
    closePdfModal() {
      this.showPdfModal = false;
    },
    formatNumber(value) {
      return value.toString().padStart(2, '0');
    },
    incrementTime(field) {
      if (field === 'hour') {
        this.time.hour = this.time.hour < 12 ? this.time.hour + 1 : 1;
      } else if (field === 'minute') {
        this.time.minute = this.time.minute < 59 ? this.time.minute + 1 : 0;
      }
    },
    decrementTime(field) {
      if (field === 'hour') {
        this.time.hour = this.time.hour > 1 ? this.time.hour - 1 : 12;
      } else if (field === 'minute') {
        this.time.minute = this.time.minute > 0 ? this.time.minute - 1 : 59;
      }
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
    confirmSettings() {
      const maxDay = this.getMaxDay();
      if (this.period.day > maxDay) {
        this.period.day = maxDay;
      }
      console.log('Time:', `${this.time.hour}:${this.time.minute} ${this.time.amPm}`);
      console.log('Period:', `${this.period.type} on day ${this.period.day}`);
    }
  }
};
</script>

<style scoped>
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

.side-bar {
    width: 350px;
    height: 100%;
    background-color: #25253C;
    color: white;
    position: fixed;
    top: 0;
    left: 0;
    transform: translateX(-100%);
    transition: transform 0.4s cubic-bezier(0.25, 1, 0.5, 1);
    z-index: 1000;
    padding-top: 60px;
}

.side-bar--visible {
    transform: translateX(0);
}

.close-button  {
    background: none;
    border: none;
    color: white;
    position: absolute;
    top: 10px;
    right: 13px;
    font-size: 24px;
    cursor: pointer;
}

.sidebar-logo {
    display: flex;
    align-items: center;
    padding-top: 30px;
    padding-left: 20px;
    padding-bottom: 0;
}

.logo-icon {
    margin-right: 10px;
    font-size: 32px;
}

.logo {
    width: 150px;
    height: auto;
}

.divider_top {
    height: 2px;
    background: white;
    margin: 40px 20px;
    opacity: 0.8;
}

.menu-options, .bottom-options {
    display: flex;
    flex-direction: column;
    margin-top: 20px;
}

.menu-option, .bottom-option {
    display: flex;
    align-items: center;
    text-align: left;
    padding: 15px 35px;
    margin: 10px;
    width: 85%;
    border-radius: 8px;
    line-height: 40px;
    background: none;
    border: none;
    color: white;
    font-size: 24px;
    font-weight: bold;
    cursor: pointer;
    transition: all 0.4s ease;
    font-family: "Wix Madefor Display", sans-serif;
}

.icon {
    margin-right: 30px;
    font-size: 24px;
}

.icon.a {
    margin-right: 15px;
}
.menu-option:hover, .bottom-option:hover {
    background-color: #3B3B5A;
    transform: translateX(10px);
}

.divider_bottom {
    height: 2px;
    background: white;
    margin: 190px 20px;
    opacity: 0.8;
}

.bottom-options {
    margin-top: -180px;
}

.bottom-option {
    font-size: 22px;
}

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
    background: white;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
    width: 500px;
    position: relative; 
}

.modal-close-icon {
    position: absolute;
    top: 15px;
    right: 18px;
    background: none;
    border: none;
    font-size: 30px;
    color: #333;
    cursor: pointer;
}

.modal-close-icon:hover {
    color: #555;
}

.section {
  margin: 20px 10px;
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
}

.time-button {
    margin-left: 10px;
    padding: 10px 20px;
    background:  #25253C;
    border: none;
    border-radius: 12px;
    color: white;
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
    background-color: #636389;
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
    padding: 15px 30px;
    background-color: #4caf50;
    border: none;
    border-radius: 12px;
    color: white;
    cursor: pointer;
    font-size: 20px;
    font-weight: bold;
    font-family: "Wix Madefor Display", sans-serif;
}

.confirm-button:hover {
    background:  #237242;
}
</style>

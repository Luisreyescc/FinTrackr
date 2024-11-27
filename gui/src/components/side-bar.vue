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
	<font-awesome-icon :icon="['fas', 'chart-pie']" class="icon a"/>Categories Pie</button>
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
      <h2>PDF Report</h2>
      <button @click="closePdfModal" class="modal-close-icon">
        <font-awesome-icon :icon="['fas', 'xmark']"/>
      </button>
      
      <div class="time-selector">
        <h3>Set Time</h3>
        <div class="time-controls">
          <button @click="incrementTime('hour')" class="arrow-button">
            <font-awesome-icon :icon="['fas', 'angle-up']" />
          </button>
          <span>{{ formatNumber(time.hour) }}</span>
          <button @click="decrementTime('hour')" class="arrow-button">
            <font-awesome-icon :icon="['fas', 'angle-down']" />
          </button>
          :
          <button @click="incrementTime('minute')" class="arrow-button">
            <font-awesome-icon :icon="['fas', 'angle-up']" />
          </button>
          <span>{{ formatNumber(time.minute) }}</span>
          <button @click="decrementTime('minute')" class="arrow-button">
            <font-awesome-icon :icon="['fas', 'angle-down']" />
          </button>
          <button @click="toggleAmPm" class="period-button">
            {{ time.amPm }}
          </button>
        </div>
      </div>
      
      <div class="period-selector">
        <h3>Set Period</h3>
        <div class="period-controls">
          <button @click="incrementPeriod('type')" class="arrow-button">
            <font-awesome-icon :icon="['fas', 'angle-up']" />
          </button>
          <span>{{ period.type }}</span>
          <button @click="decrementPeriod('type')" class="arrow-button">
            <font-awesome-icon :icon="['fas', 'angle-down']" />
          </button>
          <button @click="incrementPeriod('day')" class="arrow-button">
            <font-awesome-icon :icon="['fas', 'angle-up']" />
          </button>
          <span>{{ period.day }}</span>
          <button @click="decrementPeriod('day')" class="arrow-button">
            <font-awesome-icon :icon="['fas', 'angle-down']" />
          </button>
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
        hour: 8,
        minute: 0,
        amPm: 'AM'
      },
      period: {
        type: 'Monthly',
        day: 1
      },
      periodTypes: ['Monthly', 'Bimonthly', 'Quarterly'],
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
    padding: 20px 30px;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    text-align: center;
    width: 300px;
    height: 500px;
    position: relative; 
}

.modal-close-icon {
    position: absolute;
    top: 10px;
    right: 10px;
    background: none;
    border: none;
    font-size: 20px;
    color: #333;
    cursor: pointer;
}

.modal-close-icon:hover {
    color: #555;
}

.arrow-button {
  background: none;
  border: none;
  cursor: pointer;
}

.period-button {
  margin-left: 10px;
  padding: 5px 10px;
  background: #eee;
  border: 1px solid #ccc;
  border-radius: 4px;
  cursor: pointer;
}

.time-controls,
.period-controls {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
}

.confirm-button {
  margin-top: 20px;
  padding: 10px 20px;
  font-size: 16px;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
</style>

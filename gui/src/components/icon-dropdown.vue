<template>
<div class="icons-wrapper">
  <div class="icons-select" @click.stop="toggleDropdown">
    Icon
    <span class="dropdown-icon">
      <font-awesome-icon v-if="!dropdownOpen" :icon="['fas', 'angle-right']"/>
      <font-awesome-icon v-else :icon="['fas', 'angle-down']"/>
    </span>
  </div>
  
  <ul v-if="dropdownOpen" class="icons-dropdown">
    <li
      v-for="(icon, index) in iconOptions"
      :key="index"
      class="icon-item"
      @click="handleOptionClick(icon)"
      :class="{ active: JSON.stringify(currentIcon) === JSON.stringify(icon) }">
      <font-awesome-icon :icon="icon"/>
    </li>
  </ul>
</div>
</template>

<script>
export default {
  name: "IconDropdown",
  props: {
    iconOptions: {
      type: Array,
      required: true
    },
    currentIcon: {
      type: Array,
      default: () => []
    },
  },
  data() {
    return {
      dropdownOpen: false
    };
  },
  methods: {
    toggleDropdown() {
      this.dropdownOpen = !this.dropdownOpen;
    },
    handleOptionClick(icon) {
      this.selectIcon(icon);  
      this.dropdownOpen = false;
    },
    selectIcon(icon) {
      this.$emit("iconSelected", icon);
    }
  },
};
</script>

<style scoped>
.icons-wrapper {
    position: relative;
}

.icons-select {
    padding: 15px 20px;
    border: 1px solid #CCC;
    border-radius: 3px;
    cursor: pointer;
    display: flex;
    align-items: center;
    width: 60px;
    font-size: 18px;
    font-weight: bold;
    color: #25262B;
    background-color: white;
    box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1);
    transition: background-color 0.2s;
    font-family: "Wix Madefor Display", sans-serif;
}

.icons-select:hover {
    background-color: #F8F9FA;
}

.dropdown-icon {
    width: 16px;
    height: 16px;
    margin-left: 16px;
    transform: translateY(-3px);
    color: #25262B;
}

.icons-dropdown {
    position: absolute;
    top: 80%;
    left: 0;
    right: 0;
    border: 1px solid white;
    border-radius: 12px;
    background-color: white;
    box-shadow: 0px 4px 8px rgba(255, 255, 255, 0.1);
    z-index: 1000;
    padding: 10px;
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 10px;
    width: 300px;
    max-height: 250px;
    overflow-y: auto;
}

.icons-dropdown li {
    display: flex;
    justify-content: center;
    align-items: center;
    cursor: pointer;
    transition: background-color 0.3s, color 0.3s;
    text-align: center;
    color: #25262B;
    font-size: 36px;
    font-weight: bold;
    background-color: transparent;
    border-radius: 8px;
}

.icon-item {
    width: 60px;
    height: 60px;
    display: flex;
    justify-content: center;
    align-items: center;
    cursor: pointer;
    transition: background-color 0.3s, transform 0.2s;
    border: 1px solid transparent;
    border-radius: 8px;
}

.icon-item.active {
    background-color: #E9ECEF;
    border-color: #ADB5BD;
}

.icon-item:hover {
    background-color: #F1F3F5;
    transform: scale(1.05);
}
</style>

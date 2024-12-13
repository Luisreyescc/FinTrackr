<template>
<div class="filter-button-container" @click.stop="toggleDropdown">
  <button class="filter-button">
    <font-awesome-icon :icon="['fas', 'filter']" class="icon"/>
  </button>
  <ul v-if="dropdownOpen" class="filters-dropdown">
    <li
      v-for="(option, index) in filterOptions"
      :key="index"
      @click="selectFilter(option)"
      :class="{ active: currentFilter === option }">
      {{ option }}
    </li>
  </ul>
</div>
</template>

<script>
export default {
  name: "FilterDropdown",
    props: {
    filterOptions: {
      type: Array,
      required: true
    },
    currentFilter: {
      type: String,
      default: ""
    }
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
    handleOptionClick(option) {
      this.selectFilter(option);
      this.dropdownOpen = false;
    },
    selectFilter(option) {
      this.$emit("filterSelected", option);
    }
  }
};
</script>

<style scoped>
.filter-button-container {
    position: relative;
    padding: 12px;
}

.filter-button {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 50px;
    height: 50px;
    border-radius: 50px;
    background: white;
    border: 1px solid white;
    box-shadow: 0 4px 6px rgba(255, 255, 255, 0.1);
    cursor: pointer;
    transition: transform 0.2s ease-in-out, box-shadow 0.2s;
}

.filter-button:hover {
    box-shadow: 0 6px 10px rgba(255, 255, 255, 0.15);
    transform: scale(1.1);
}

.icon {
    color: #25262B;
    font-size: 24px;
}

.filters-dropdown {
    position: absolute;
    top: 50px;
    right: 0;
    border: 1px solid #3F4049;
    border-radius: 12px;
    background-color: #404149;
    box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
    padding: 0;
    list-style: none;
    z-index: 1000;
    min-width: 135px;
    animation: fadeIn 0.2s ease-out;
}

.filters-dropdown li {
    padding: 20px 30px;
    cursor: pointer;
    transition: background-color 0.3s ease, color 0.3s ease, transform 0.2s ease, box-shadow 0.2s ease;
    text-align: left;
    color: white;
    font-weight: bold;
    overflow: visible;
}

.filters-dropdown li:hover {
    background-color: white;
    border-radius: 12px;
    color: #25262B;
    font-weight: bold;
}
</style>

<template>
  <div class="filter-button-container" @click.stop="toggleDropdown">
    <button class="filter-button">
      <font-awesome-icon :icon="['fas', 'filter']" />
    </button>
    <ul v-if="dropdownOpen" class="filters-dropdown">
      <li
        v-for="(option, index) in filterOptions"
        :key="index"
        @click="selectFilter(option)"
        :class="{ active: currentFilter === option }" >
        {{ option }}
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: "FilterGraphics",
    props: {
    filterOptions: {
      type: Array,
      required: true,
    },
    currentFilter: {
      type: String,
      default: "",
    },
  },
  data() {
    return {
      dropdownOpen: false,
    };
  },
  methods: {
    toggleDropdown() {
      this.dropdownOpen = !this.dropdownOpen;
    },
    selectFilter(option) {
      this.$emit("filterSelected", option);
      this.dropdownOpen = false;
    },
  },
};
</script>

<style scoped>
.filter-button-container {
    position: relative;
    padding: 12px;
}

.filter-button {
    background: white;
    border: 2px solid #ddd;
    border-radius: 50%;
    cursor: pointer;
    color: #333;
    font-size: 20px;
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease;
}

.filter-button:hover {
    border-color: #21255b;
    box-shadow: 0 6px 10px rgba(0, 0, 0, 0.15);
    transform: scale(1.1);
}

.filters-dropdown {
    position: absolute;
    top: 50px;
    right: 0;
    border: 1px solid #ddd;
    border-radius: 12px;
    background-color: white;
    box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
    padding: 0;
    list-style: none;
    z-index: 1000;
    min-widht: 120px;
    animation: fadeIn 0.2s ease-out;
}

.filters-dropdown li {
    padding: 10px 20px;
    cursor: pointer;
    transition: background-color 0.3s, color 0.3s;
    text-align: left;
    overflow: visible;
}

.filters-dropdown li:hover {
    background-color: #f0f8ff;
    border-radius: 12px;
    color: #1010AC;
    font-weight: bold;
}
</style>

<template>
    <div class="search-bar">
      <input
        type="text"
        v-model="searchQuery"
        @input="onSearch"
        placeholder="Search..."
        class="search-input"
      />
      <font-awesome-icon :icon="['fas', 'search']" class="search-icon" />
    </div>
  </template>
  
  <script>
  export default {
    name: "SearchBar",
    props: {
      data: {
        type: Array,
        default: () => [],
      },
    },
    data() {
      return {
        searchQuery: "",
      };
    },
    methods: {
      onSearch() {
        this.$emit('search', this.searchQuery);
      },
    },
  };
  </script>
  
  <style scoped>
  .search-bar {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 5px;
    background-color: #f4f4f4;
    border-radius: 20px;
  }
  
  .search-input {
    border: none;
    padding: 8px;
    font-size: 16px;
    border-radius: 15px;
    margin-right: 10px;
    width: 200px;
  }
  
  .search-input:focus {
    outline: none;
    border-color: #00A0BE;
  }
  
  .search-icon {
    font-size: 20px;
    color: #00A0BE;
  }
  </style>
<template>
<div class="search-bar">
  <div class="search-container">
    <font-awesome-icon :icon="['fas', 'magnifying-glass']" class="search-icon"/>
    <input type="text" v-model="searchQuery" @input="onSearch" placeholder="Search..." class="search-bar"/>
  </div>
</div>
</template>
  
<script>
export default {
  name: "SearchBar",
  props: {
    data: {
      type: Array,
      default: () => []
      }
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
.search-container {
    flex: 1;
    position: relative;
    display: flex;
    align-items: center;
    background: #ffffff;
    border-radius: 50px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.search-icon {
    position: absolute;
    left: 20px;
    color: #25262B;
    font-size: 20px;
}

.search-bar {
    width: 100%;
    padding: 21px 50px 21px 50px;
    border: none;
    border-radius: 50px;
    font-size: 20px;
    color: #333;
    background: transparent;
    outline: none;
    box-shadow: none;
}

.search-bar::placeholder {
    color: #25262B;
    font-size: 20px;
}
</style>

<template>
 <div class="history-header">
   <div class="search-container">
     <font-awesome-icon :icon="['fas', 'magnifying-glass']" class="search-icon"/>
     <input
       type="text"
       class="search-bar"
       placeholder="Search..."
       v-model="searchQuery"
       @input="onSearch"/>
   </div>
   
   <FilterDropdown
     :filterOptions="['Category:', 'Amount ==', 'Description:', 'Date:', 'Amount >=', 'Amount <=']"
     :currentFilter="currentFilter"
     @filterSelected="applyFilter"/>
   
   <button @click="resetFilters" class="reset-button" >
     <font-awesome-icon :icon="['fas', 'clock-rotate-left']" class="icon"/>
   </button>
 </div>
</template>

<script>
import FilterDropdown from "@/components/filter-dropdown.vue";
  
export default {
  name: "HistoryHeader",
  components: {
    FilterDropdown
  },
  data() {
    return {
      currentFilter: "All",
      searchQuery: ""
   };
  },
  methods: {
    applyFilter(filter) {
      this.searchQuery = filter;
      this.$emit('search', this.searchQuery);
    },
    onSearch(event) {
      this.searchQuery = event.target.value;
      this.$emit('search', this.searchQuery);
    },
    resetFilters() {
      this.searchQuery = "";
      this.$emit('resetClicked');
    }
  },
};
</script>

<style scoped>
.history-header {
    display: flex;
    align-items: center;
    gap: 20px;
    padding: 10px 20px;
    background-color: none;
}

.search-container {
    flex: 1;
    position: relative;
    display: flex;
    align-items: center;
    background: #ffffff;
    border-radius: 50px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    min-width: 100px;
    max-width: 600px;
}

.search-icon {
    position: absolute;
    left: 20px;
    color: #25262B;
    font-size: 20px;
}

.search-bar {
    width: 100%;
    padding: 21px 200px 21px 50px;
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

.reset-button {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 50px;
    height: 50px;
    border-radius: 50px;
    background: #25262B;
    border: 1px solid #25262B;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    cursor: pointer;
    transition: transform 0.2s ease-in-out, box-shadow 0.2s;
}

.icon {
    color: white;
    font-size: 24px;
}

.reset-button:hover {
    box-shadow: 0 6px 10px rgba(0, 0, 0, 0.15);
    transform: scale(1.1);
}
</style>

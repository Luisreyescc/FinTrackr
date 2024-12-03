<template>
<div class="history-header">
  <div class="search-container">
    <font-awesome-icon :icon="['fas', 'magnifying-glass']" class="search-icon"/>
    <div class="tags-input">
      <span v-for="(tag, index) in selectedFilters" :key="index" class="tag">
        {{ tag }}
        <button class="tag-remove" @click="removeFilter(index)">
          <font-awesome-icon :icon="['fas', 'times']" />
        </button>
      </span>
      <input
	type="text"
	class="search-bar"
	placeholder="Search..."
	@input="$emit('search', $event.target.value)"/>
    </div>
  </div>
  
  <FilterDropdown
    :filterOptions="['All', 'Category:', 'Amount ==:', 'Description:', 'Date:', 'Amount >=:', 'Amount <=:']"
    :currentFilter="currentFilter"
    @filterSelected="applyFilter" />
  
  <button @click="$emit('resetClicked')" class="reset-button" >
    <font-awesome-icon :icon="['fas', 'clock-rotate-left']" class="icon" />
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
      selectedFilters: []
    };
  },
  methods: {
    applyFilter(filter) {
      this.selectedFilters.push(filter);
    },
    removeFilter(index) {
      this.selectedFilters.splice(index, 1);
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
    color: #aaa;
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
    color: #aaa;
    font-size: 20px;
}

.reset-button {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 50px;
    height: 50px;
    border-radius: 50px;
    background: #ffffff;
    border: 1px solid #ddd;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    cursor: pointer;
    transition: transform 0.2s ease-in-out, box-shadow 0.2s;
}

.icon {
    color: #aaa;
    font-size: 24px;
}

.reset-button:hover {
    box-shadow: 0 6px 10px rgba(0, 0, 0, 0.15);
    transform: scale(1.1);
}

.tag {
  display: flex;
  align-items: center;
  padding: 5px 10px;
  font-size: 14px;
  border-radius: 12px;
  background: #f5f5fc;
  color: #333;
  border: 1px solid #ddd;
}

/* Botón para eliminar etiquetas */
.tag-remove {
  background: none;
  border: none;
  margin-left: 8px;
  color: #555;
  cursor: pointer;
}

.tag-remove:hover {
  color: #ff5a5a;
}
</style>

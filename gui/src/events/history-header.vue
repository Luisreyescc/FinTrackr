<template>
<div class="history-header">
  <div class="search-container">
   <font-awesome-icon :icon="['fas', 'magnifying-glass']" class="search-icon" />
   <input
     type="text"
     class="search-bar"
     placeholder="Search..."
     @input="$emit('search', $event.target.value)"/>
  </div>
  <div class="filter-button-container" @click.stop="toggleDropdown">
    <button class="filter-button">
      <font-awesome-icon :icon="['fas', 'filter']" class="icon"/>
    </button>
    <ul v-if="dropdownOpen" class="filters-dropdown">
    </ul>
  </div>
  <button @click="$emit('resetClicked')" class="reset-button" >
    <font-awesome-icon :icon="['fas', 'clock-rotate-left']" class="icon" />
  </button>
</div>
</template>

<script>
export default {
  name: "HistoryHeader",
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
    background: #ffffff;
    border: 1px solid #ddd;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    cursor: pointer;
    transition: transform 0.2s ease-in-out, box-shadow 0.2s;
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

.filter-button:hover, .reset-button:hover {
    box-shadow: 0 6px 10px rgba(0, 0, 0, 0.15);
    transform: scale(1.1);
}
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
    color: #aaa;
    font-size: 20px;
}

.search-bar {
    width: 100%;
    padding: 21px 26px 21px 50px;
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
    right: 15px;
}
</style>

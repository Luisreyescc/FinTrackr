<template>
<transition name="fade-up" @after-leave="$emit('close')">
  <div :class="['message', messageType]" v-if="visible">
    <div class="message-content">
      <span class="message-text">{{ text }}</span>
    </div>
    <button class="close-button" @click="closeMessage">
      <font-awesome-icon :icon="['fas', 'xmark']" class="close-button"/>
    </button>
  </div>
</transition>
</template>

<script>
export default {
  name: "MessageAlerts",
  props: {
    text: {
      type: String,
      required: true
    },
    type: {
      type: String,
      default: "neutral"
    }
  },
  data() {
    return {
      visible: true
    };
  },
  computed: {
    messageType() {
      return {
        success: "message-success",
        error: "message-error",
        neutral: "message-neutral"
      }[this.type] || "message-neutral";
    }
  },
  mounted() {
    this.autoClose();
  },
  methods: {
    closeMessage() {
      this.visible = false;
    },
    autoClose() {
      setTimeout(() => {
	this.visible = false;
      }, 6000);
    }
  }
};
</script>

<style scoped>
.message {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    padding: 15px;
    border-radius: 8px;
    box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
    margin-bottom: 10px;
    font-family: "Wix Madefor Display", sans-serif;
    position: fixed;
    bottom: 50px;
    left: 50%;
    transform: translateX(-50%);
    max-width: 90%;
    transition: opacity 0.5s ease, transform 0.5s ease;
    opacity: 1;
    z-index: 1000;
}

.fade-up-enter-active,
.fade-up-leave-active {
    transition: opacity 0.5s ease, transform 0.5s ease;
}

.fade-up-enter, 
.fade-up-leave-to {
    opacity: 0;
    transform: translateY(10px);
}

.message-hidden {
    opacity: 0;
    transform: translateX(-50%) translateY(10px);
}

.message-success {
    background-color: #e0f7e9;
    color: #2e7d32;
}

.message-error {
    background-color: #ffebee;
    color: #c62828;
}

.message-neutral {
    background-color: #e3f2fd;
    color: #1976d2;
}

.message-content {
    flex: 1;
    padding-right: 10px;
}

.message-text {
    flex: 1;
}

.close-button {
    background: none;
    border: none;
    padding: 0;
    cursor: pointer;
    color: inherit;
    display: flex;
    align-items: center;
    justify-content: center;
}
</style>

<template>
  <div :class="['message', messageType]" v-if="visible">
    <div class="message-content">
      <span class="message-text">{{ text }}</span>
    </div>
    <button class="close-button" @click="closeMessage">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 384 512" width="16" height="16" fill="currentColor">
	<path d="M342.6 150.6c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0L192 210.7 86.6 105.4c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3L146.7 256 41.4 361.4c-12.5 12.5-12.5 32.8 0 45.3s32.8 12.5 45.3 0L192 301.3 297.4 406.6c12.5 12.5 32.8 12.5 45.3 0s12.5-32.8 0-45.3L237.3 256 342.6 150.6z"/>
      </svg>
    </button>
  </div>
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
      default: "neutral",
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
      }, 11000);
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

.close-button svg {
    width: 16px;
    height: 16px;
    fill: currentColor;
}
</style>

<template>
  <div class="username-input">
    <label for="username">Username</label>
    <div class="username-container">
      <span class="user-icon gg-user"></span>
      <input
        v-model="localUsername"
        type="text"
        id="username"
        placeholder="Username..."
        :class="{ 'input-error': hasError, 'padded-input': true }"
        @input="validateUsername"
      />
    </div>
    <span v-if="hasError" class="error-message">{{ errorMessage }}</span>
  </div>
  
  <div class="message-container">
    <MessageAlerts
      v-for="(msg, index) in messages"
      :key="msg.id"
      :text="msg.text"
      :type="msg.type"
      @close="removeMessage(index)" />
  </div>
</template>

<script>
import MessageAlerts from "@/components/messages.vue";

export default {
  name: "UsernameInput",
  components: { MessageAlerts },
  props: {
    modelValue: String,
  },
  data() {
    return {
      localUsername: this.modelValue || "",
      errorMessage: "",
      hasError: false,
      messages: [],
    };
  },
  watch: {
    modelValue(newValue) {
      this.localUsername = newValue;
      this.validateUsername();
    },
    localUsername(newValue) {
      this.$emit("update:modelValue", newValue);
    },
  },
  methods: {
    validateUsername() {
      this.errorMessage = "";
      this.hasError = false;

      if (!this.localUsername) {
        this.setError("Username is required");
      } else if (this.localUsername.length < 3) {
        this.setError("Username must be at least 3 characters long");
      } else if (this.localUsername.length > 16) {
        this.setError("Username must be 16 characters or less");
      }
    },
    setError(message) {
      this.errorMessage = message;
      this.hasError = true;
      this.$emit("error", message);
    },
    addMessage(text, type = "neutral") {
      const id = Date.now();
      this.messages.push({ id, text, type });
    },
    removeMessage(index) {
      this.messages.splice(index, 1);
    },
  },
};
</script>

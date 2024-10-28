<template>
  <h3>Welcome to FinTrackr {{getUsername()}}</h3>
</template>

<script>
import {  GET_USERNAME } from "../store/storeconstants";
export default {
    name: 'WelcomeView',
    data() {
        return {
        }
    },
    methods:{
        getUsername() {
            return this.$store.getters[`auth/${GET_USERNAME}`]
        }, 
    }
}
</script>

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { library } from '@fortawesome/fontawesome-svg-core';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';

import {
  faUser,
  faEnvelope,
  faKey,
  faChartLine,
  faCreditCard,
  faXmark,
  faPenToSquare, 
  faRightFromBracket, 
  faCircleDollarToSlot, 
  faMoneyBillTransfer, 
  faAngleRight, 
  faAngleDown 
} from '@fortawesome/free-solid-svg-icons';

import { faDocker } from '@fortawesome/free-brands-svg-icons';

library.add(
  faUser,
  faEnvelope,
  faKey,
  faChartLine,
  faCreditCard,
  faDocker,
  faXmark,
  faPenToSquare,
  faRightFromBracket,
  faCircleDollarToSlot,
  faMoneyBillTransfer,
  faAngleRight,
  faAngleDown
);

const app = createApp(App)
app.component('font-awesome-icon', FontAwesomeIcon);
app.use(router)
app.mount('#app')

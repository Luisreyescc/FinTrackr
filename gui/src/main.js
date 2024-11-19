import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { library } from '@fortawesome/fontawesome-svg-core';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';

import {
  faUser,
  faEnvelope,
  faKey,
  faBars,
  faXmark,
  faChartLine,
  faCreditCard,
  faPenToSquare, 
  faRightFromBracket,
  faIdCard,
  faPassport,
  faCakeCandles,
  faPlus,
  faAngleRight, 
  faAngleDown ,
  faCircleDollarToSlot, 
  faMoneyBillTransfer,
  faFilter
} from '@fortawesome/free-solid-svg-icons';

import { faDocker } from '@fortawesome/free-brands-svg-icons';

library.add(
  faUser,
  faEnvelope,
  faKey,
  faBars,
  faDocker,
  faXmark,
  faChartLine,
  faCreditCard,
  faPenToSquare,
  faRightFromBracket,
  faIdCard,
  faPassport,
  faCakeCandles,
  faPlus,
  faAngleRight,
  faAngleDown,
  faCircleDollarToSlot,
  faMoneyBillTransfer,
  faFilter
);

const app = createApp(App)
app.component('font-awesome-icon', FontAwesomeIcon);
app.use(router)
app.mount('#app')

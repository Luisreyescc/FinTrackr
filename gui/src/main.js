import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { library } from '@fortawesome/fontawesome-svg-core';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';

import {
  faCheck,
  faUser,
  faUsers,
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
  faAngleDown,
  faCircleDollarToSlot, 
  faMoneyBillTransfer,
  faFilter,
  faTrashCan,
  faChartPie,
  faChartArea,
  faPiggyBank,
  faHandHoldingDollar,
  faEnvelopeOpenText,
  faAngleUp,
  faClockRotateLeft,
  faMagnifyingGlass,
  faCalendar,
  faUserTie,
  faCircleInfo,
  faHandshake,
  faMoneyBills,
  faSackDollar,
  faCommentsDollar,
  faStore,
  faShop,
  faCartShopping,
  faBagShopping,
  faSuitcaseMedical,
  faHeartPulse,
  faStethoscope,
  faSyringe,
  faPills,
  faTooth,
  faHospital,
  faHandHoldingMedical,
  faGift,
  faHouseChimney,
  faHeart,
  faDumbbell,
  faBurger,
  faPizzaSlice,
  faHotdog,
  faIceCream,
  faUtensils,
  faBowlFood,
  faDrumstickBite,
  faShrimp,
  faMugHot,
  faChampagneGlasses,
  faMartiniGlassCitrus,
  faFerry,
  faCar,
  faTrainSubway,
  faPlaneDeparture,
  faHotel,
  faSchool,
  faBuilding,
  faUmbrellaBeach,
  faGasPump,
  faShirt,
  faFilm,
  faTicket,
  faGamepad,
  faMobile,
  faTv,
  faHeadphonesSimple,
  faMicrophone,
  faVideo,
  faCameraRetro,
  faMusic,
  faFutbol,
  faPersonSwimming,
  faBasketball,
  faBicycle
} from '@fortawesome/free-solid-svg-icons';

import {
  faDocker,
  faGithub,
  faGitlab,
  faLinux,
  faYoutube,
  faTwitch,
  faSteam,
  faSpotify,
  faApple,
  faAndroid,
  faXbox,
  faPlaystation
} from '@fortawesome/free-brands-svg-icons';

library.add(
  faCheck,
  faUser,
  faUsers,
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
  faFilter,
  faTrashCan,
  faChartPie,
  faChartArea,
  faPiggyBank,
  faHandHoldingDollar,
  faEnvelopeOpenText,
  faAngleUp,
  faClockRotateLeft,
  faMagnifyingGlass,
  faCalendar,
  faUserTie,
  faCircleInfo,
  faHandshake,
  faMoneyBills,
  faSackDollar,
  faCommentsDollar,
  faStore,
  faShop,
  faCartShopping,
  faBagShopping,
  faHeartPulse,
  faSuitcaseMedical,
  faStethoscope,
  faSyringe,
  faPills,
  faTooth,
  faHospital,
  faHandHoldingMedical,
  faGift,
  faHouseChimney,
  faDumbbell,
  faHeart,
  faBurger,
  faPizzaSlice,
  faHotdog,
  faIceCream,
  faUtensils,
  faBowlFood,
  faDrumstickBite,
  faShrimp,
  faMugHot,
  faChampagneGlasses,
  faMartiniGlassCitrus,
  faFerry,
  faCar,
  faTrainSubway,
  faPlaneDeparture,
  faHotel,
  faSchool,
  faBuilding,
  faUmbrellaBeach,
  faGasPump,
  faShirt,
  faFilm,
  faTicket,
  faGamepad,
  faMobile,
  faTv,
  faHeadphonesSimple,
  faMicrophone,
  faVideo,
  faCameraRetro,
  faMusic,
  faFutbol,
  faPersonSwimming,
  faBasketball,
  faBicycle,
  faGitlab,
  faGithub,
  faLinux,
  faYoutube,
  faTwitch,
  faSteam,
  faSpotify,
  faApple,
  faAndroid,
  faXbox,
  faPlaystation
);

const app = createApp(App)
app.component('font-awesome-icon', FontAwesomeIcon);
app.use(router)
app.mount('#app')

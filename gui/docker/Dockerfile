FROM node:18

WORKDIR /gui

COPY package*.json ./

RUN npm install vuex@next vue-router axios apexcharts vue3-apexcharts moment

RUN npm install --save @fortawesome/fontawesome-svg-core @fortawesome/free-solid-svg-icons @fortawesome/free-brands-svg-icons @fortawesome/vue-fontawesome

COPY . /gui

EXPOSE 8080

CMD ["npm", "run", "serve"]

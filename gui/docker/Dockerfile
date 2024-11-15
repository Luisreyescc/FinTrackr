FROM node:18

WORKDIR /gui

COPY package*.json ./

RUN npm install vuex@next vue-router axios apexcharts vue3-apexcharts

COPY . /gui

EXPOSE 8080

CMD ["npm", "run", "serve"]

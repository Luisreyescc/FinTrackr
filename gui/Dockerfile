FROM node:18

WORKDIR /app

COPY package*.json ./

RUN npm install
RUN npm install vuex@next vue-router --save
RUN npm install axios

COPY . .

EXPOSE 8080

CMD ["npm", "run", "serve"]

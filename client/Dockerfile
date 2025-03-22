FROM node:lts-alpine

WORKDIR /app

COPY package.json package-lock.json vite.config.js ./

RUN npm install -f 

RUN npm i -g serve

COPY . .

RUN npm run build

EXPOSE 3000

CMD [ "serve", "-s", "dist" ]
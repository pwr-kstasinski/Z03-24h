### STAGE 1: Build ###
FROM node:16 AS build
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm install
COPY . .
RUN npm run build
### STAGE 2: Run ###
FROM nginx:1.21.0

COPY --from=build /app/dist/MessengerApp /usr/share/nginx/html
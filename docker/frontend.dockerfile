FROM node:latest as build-stage
ARG BASE_URL
WORKDIR /app
COPY ./frontend/package.json ./
RUN npm install
COPY ./frontend .
RUN npm run build

FROM nginx:latest as production-stage
RUN mkdir /app
COPY --from=build-stage /app/dist /app
COPY ./docker/nginx.conf /etc/nginx/nginx.conf
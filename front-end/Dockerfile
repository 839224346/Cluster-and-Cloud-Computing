FROM node:alpine

ENV http_proxy http://wwwproxy.unimelb.edu.au:8000/
ENV https_proxy http://wwwproxy.unimelb.edu.au:8000/

RUN mkdir /app

WORKDIR '/app'

COPY package.json /app

RUN npm install

COPY . /app

RUN npm run build
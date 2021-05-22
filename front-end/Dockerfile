FROM node:alpine

ENV http_proxy http://wwwproxy.unimelb.edu.au:8000/
ENV https_proxy http://wwwproxy.unimelb.edu.au:8000/

WORKDIR '/app'

COPY package.json .
RUN npm install
COPY . .
CMD ["npm", "start"]
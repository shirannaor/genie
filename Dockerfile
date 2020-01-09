FROM node:12-alpine3.9
EXPOSE 3000
WORKDIR /service

# RUN npm i -g yarn

COPY ./package.json .

RUN yarn

COPY src /service/src
COPY public /service/public

RUN yarn build

CMD yarn serve -s build -l 3000 --no-clipboard
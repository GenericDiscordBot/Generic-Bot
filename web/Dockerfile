FROM node:alpine

WORKDIR /web

ENV PATH /web/node_modules/.bin:$PATH

COPY ./components ./pages ./public ./next-env.d.ts ./next.config.js ./package.json ./tsconfig.json ./

RUN yarn install

CMD ["npm", "start"]

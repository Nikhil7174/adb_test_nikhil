# Use Node.js 16 to avoid compatibility issues
FROM node:16-alpine

WORKDIR /src/app

COPY package.json yarn.lock ./

RUN yarn install --frozen-lockfile

COPY . .

CMD ["yarn", "start"]
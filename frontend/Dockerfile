# Stage 1: Build Stage
FROM node:22-alpine3.19 AS builder

WORKDIR /app

COPY package*.json ./

RUN npm ci

COPY . ./

RUN npm run build

RUN npm prune --production

# Stage 2: Production Stage
FROM node:22-alpine3.19

WORKDIR /app

COPY --from=builder /app/build ./build
COPY --from=builder /app/node_modules ./node_modules
COPY package.json ./

EXPOSE 3000

ENV NODE_ENV=production

CMD ["node", "build"]

# Stage 3: Development Stage (optional)
FROM node:22-alpine3.19 AS development

WORKDIR /app

RUN yarn global add nodemon

COPY package*.json ./

RUN npm ci

COPY . ./

EXPOSE 3000

ENV NODE_ENV=development

CMD ["nodemon", "--watch", "/app", "--exec", "npm", "run", "dev"]

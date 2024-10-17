# Build stage
FROM node:22-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . ./
RUN npm run build
RUN npm prune --production

# Production stage
FROM node:22-alpine AS production
WORKDIR /app
COPY --from=builder /app/build build/
COPY --from=builder /app/node_modules node_modules/
COPY package.json ./
EXPOSE 3000
ENV NODE_ENV=production
CMD [ "node", "build" ]

# Development stage
FROM node:22-alpine AS development
WORKDIR /app
RUN npm install --global nodemon
COPY package*.json ./
RUN npm ci
COPY . ./
EXPOSE 3000
ENV NODE_ENV=development
FROM node:alpine as builder

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN ls -la
RUN npm run build

# Stage 2: Setup the production environment
FROM node:alpine

WORKDIR /app

# Copy only necessary directories and files
COPY --from=builder /app/build ./build
COPY --from=builder /app/node_modules ./node_modules
ENV ORIGIN=http://localhost:3000

CMD ["node", "build"]
EXPOSE 3000
# Dockerfile in parent folder

FROM node:20-alpine3.21 AS builder
WORKDIR /app
COPY usermanagement/package*.json ./
RUN npm install
COPY usermanagement/. .
RUN npm run build

FROM nginx:alpine
RUN rm -rf /usr/share/nginx/html/*
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]


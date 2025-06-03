# ---------- Stage 1: Build the React app ----------
FROM node:20-alpine AS build

# Set working directory
WORKDIR /app

# Copy package.json and lock file first (for caching)
COPY userlist-app/package*.json ./userlist-app/
WORKDIR /app/userlist-app

# Install dependencies
RUN npm install

# Copy the rest of the app
COPY userlist-app/ .

# Build the app
RUN npm run build


# ---------- Stage 2: Serve with Nginx ----------
FROM nginx:stable-alpine

# Copy build output to nginx html directory
COPY --from=build /app/userlist-app/build /usr/share/nginx/html

# Optional: use custom Nginx config to support React routing
COPY userlist-app/nginx.conf /etc/nginx/conf.d/default.conf

# Expose port
EXPOSE 80

# Run Nginx in foreground
CMD ["nginx", "-g", "daemon off;"]

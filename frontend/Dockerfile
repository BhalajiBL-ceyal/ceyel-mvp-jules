# Stage 1: Build the React application
FROM node:16-alpine as build

WORKDIR /app

# Copy package.json and package-lock.json
COPY frontend/package.json frontend/package-lock.json ./

# Install dependencies
RUN npm install

# Copy the rest of the frontend application files
COPY frontend ./

# Build the application
RUN npm run build

# Stage 2: Serve the application using Nginx
FROM nginx:stable-alpine

# Copy the built application from the build stage
COPY --from=build /app/build /usr/share/nginx/html

# Copy nginx config
COPY frontend/nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]

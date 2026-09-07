FROM node:18-alpine AS frontend-build
WORKDIR /app
COPY cloudmosaic-react-main/package*.json ./
# Use exact versions or simple install to ensure clean build
RUN npm ci || npm install
COPY cloudmosaic-react-main/ ./
ENV REACT_APP_API_URL=/api/v1
RUN npm run build

FROM nginx:alpine
COPY --from=frontend-build /app/build /usr/share/nginx/html
COPY nginx/nginx.conf /etc/nginx/conf.d/default.conf

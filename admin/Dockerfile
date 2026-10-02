FROM node:22-alpine AS build
WORKDIR /app
COPY admin/package.json ./package.json
RUN npm install --no-audit --no-fund
COPY admin/ .
RUN npm run build

FROM nginx:alpine
COPY admin/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80

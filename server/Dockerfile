FROM node:22-alpine
WORKDIR /app
COPY server/package.json ./package.json
RUN npm install --omit=dev --no-audit --no-fund
COPY server/src ./src
COPY docs/archive ./docs/archive
VOLUME /app/data
EXPOSE 3001
CMD ["sh", "-c", "[ -f data/fright-night.db ] || node src/seed.js; exec node src/index.js"]

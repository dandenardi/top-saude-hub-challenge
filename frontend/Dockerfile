FROM node:20-alpine
WORKDIR /app
COPY frontend/package*.json ./
COPY frontend/package-lock.json ./
RUN npm ci
COPY frontend/ .
ENV NEXT_TELEMETRY_DISABLED=1
RUN npm run build
EXPOSE 3000
CMD ["npm", "start"]

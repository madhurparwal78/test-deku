# Ravel — one production build, one origin, Node 20.
FROM node:20-bookworm-slim AS base
ENV NODE_ENV=production
WORKDIR /app

# ---- server dependencies ----
FROM base AS server-deps
COPY package.json package-lock.json* ./
RUN npm install --omit=dev --no-audit --no-fund

# ---- web build ----
FROM base AS web-build
COPY web/package.json web/package-lock.json* ./web/
RUN cd web && npm install --no-audit --no-fund
COPY web ./web
RUN cd web && npx vite build

# ---- server build ----
FROM base AS server-build
COPY package.json package-lock.json* ./
RUN npm install --no-audit --no-fund
COPY tsconfig.server.json ./
COPY server ./server
RUN npx tsc -p tsconfig.server.json

# ---- runtime ----
FROM base AS runtime
COPY --from=server-deps /app/node_modules ./node_modules
COPY --from=server-build /app/dist ./dist
COPY --from=web-build /app/web/dist ./web/dist
COPY package.json ./

ENV PORT=4173
EXPOSE 4173
# Migrations and seed run inside main(), against the environment's own services.
CMD ["node", "dist/index.js"]

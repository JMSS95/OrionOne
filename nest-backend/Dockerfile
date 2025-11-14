# Stage 1: Development
FROM node:20-alpine AS development

WORKDIR /app

# Install dependencies for better caching
COPY package*.json ./
RUN npm install

# Copy source code
COPY . .

# Generate Prisma Client (if prisma schema exists)
RUN if [ -f prisma/schema.prisma ]; then npx prisma generate; fi

# Expose port
EXPOSE 3001

# Start development server
CMD ["npm", "run", "start:dev"]


# Stage 2: Build
FROM node:20-alpine AS build

WORKDIR /app

# Copy dependencies
COPY package*.json ./
RUN npm ci

# Copy source code
COPY . .

# Generate Prisma Client
RUN npx prisma generate

# Build application
RUN npm run build

# Prune dev dependencies
RUN npm prune --production


# Stage 3: Production
FROM node:20-alpine AS production

WORKDIR /app

# Install dumb-init for proper signal handling
RUN apk add --no-cache dumb-init

# Create non-root user
RUN addgroup -g 1001 -S nodejs && adduser -S nestjs -u 1001

# Copy built application and production dependencies
COPY --from=build --chown=nestjs:nodejs /app/dist ./dist
COPY --from=build --chown=nestjs:nodejs /app/node_modules ./node_modules
COPY --from=build --chown=nestjs:nodejs /app/package*.json ./
COPY --from=build --chown=nestjs:nodejs /app/prisma ./prisma

# Generate Prisma Client
RUN npx prisma generate

# Switch to non-root user
USER nestjs

# Expose port
EXPOSE 3001

# Use dumb-init to handle signals properly
ENTRYPOINT ["dumb-init", "--"]

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD node -e "require('http').get('http://localhost:3001/api/health', (r) => {process.exit(r.statusCode === 200 ? 0 : 1)})"

# Start production server
CMD ["node", "dist/main"]

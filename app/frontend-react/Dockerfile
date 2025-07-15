####### BUILDER IMAGE #######
# Build stage
FROM node:alpine AS builder

WORKDIR /usr/src/app

# Copy everything else, test and build
COPY . /usr/src/app

#test the app
# Copy dependency files and install dependencies
RUN npm install && npm i --save-dev @types/jest
ENV VITE_REACT_APP_BASE_URL=https://backend.astraowl.com/
RUN npm run build

####### PRODUCTION IMAGE #######
FROM node:alpine

WORKDIR /usr/src/app

# Install 'serve' globally
RUN npm install -g serve

# Copy built assets from builder
COPY --from=builder /usr/src/app/dist ./dist

EXPOSE 80

# Serve the build on port 80
CMD ["serve", "-s", "dist", "-l", "80"]
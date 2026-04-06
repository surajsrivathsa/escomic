FROM node:19-alpine
RUN apk update && apk add git

RUN mkdir /app
WORKDIR /app

# Copy package files first
COPY package.json ./
COPY package-lock.json ./

# Install dependencies
RUN npm install --legacy-peer-deps

# Copy source code
COPY ./src /app/src

# Copy comic book covers
COPY ./public/comic_book_covers_ui/ /app/public/comic_book_covers_ui/

EXPOSE 3000
CMD ["npm", "start"]


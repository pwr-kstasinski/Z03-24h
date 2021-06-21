FROM node

COPY . /app
WORKDIR /app

# RUN npm install

HEALTHCHECK --interval=5s --timeout=5s --start-period=5s --retries=3 CMD curl --fail http://localhost:5000/healthcheck || exit 1

CMD [ "node", "server.js" ]
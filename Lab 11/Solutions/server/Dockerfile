FROM python:3

ENV DB_USER=root
ENV DB_PASSWORD=Password
ENV DB_HOST=db
ENV DB_PORT=6000
ENV HOST=localhost
ENV PORT=5000

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./your-daemon-or-script.py" ]

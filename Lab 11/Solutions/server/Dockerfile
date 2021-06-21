FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

HEALTHCHECK --interval=1s --timeout=1s --start-period=5s --retries=3 CMD curl --fail http://127.0.0.1:5000/ping || exit 1

CMD [ "python", "main.py" ]
FROM python:2.7

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

ENV FLASK_APP=app.py

EXPOSE 5000

HEALTHCHECK --interval=5s --timeout=5s --start-period=5s --retries=3 CMD curl --fail http://127.0.0.1:5000/healthcheck || exit 1

CMD ["python", "app.py"]

FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

ENV DB_USER=root
ENV DB_PASSWORD=1236
ENV DB_HOST=db
ENV DB_PORT=3306
ENV DB_NAME=messenger
ENV FA_DOCKS_URL=/docs

# uvicorn
ENV HOST=0.0.0.0
ENV PORT=8000

# uvicorn env vars
ENV MAX_WORKERS=1

WORKDIR /dock

COPY requirements.txt /dock

RUN pip install -r requirements.txt

COPY . /dock

EXPOSE ${PORT}

HEALTHCHECK --interval=15s --timeout=3s --start-period=5s CMD curl -f http://127.0.0.1:${PORT}/health_status/ || exit 1
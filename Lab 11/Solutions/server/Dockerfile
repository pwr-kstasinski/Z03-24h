FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

ENV DB_USER=root
ENV DB_PASSWORD=1236
ENV DB_HOST=db
ENV DB_PORT=3306
ENV FA_DOCKS_URL=/docs
ENV HOST=0.0.0.0
ENV PORT=8000

COPY . /dock

WORKDIR /dock

RUN pip install -r requirements.txt

EXPOSE ${PORT}

HEALTHCHECK --interval=5s --timeout=3s --start-period=5s CMD curl -f http://127.0.0.1:${PORT}/health_status/ || exit 1
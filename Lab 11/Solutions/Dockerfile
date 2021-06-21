FROM python:3.9.2

ENV DB_USER='root'
ENV DB_PASSWORD='toor'
ENV DB_HOST='0.0.0.0'
ENV DB_PORT='3306'
ENV DB_NAME='chatroomdb'

WORKDIR /CHATROOM-dir

COPY server.py /CHATROOM-dir
COPY requirements.txt .
RUN pip install -r requirements.txt


EXPOSE 5000
EXPOSE 3306
CMD ["python", "/CHATROOM-dir/server.py"]

HEALTHCHECK --interval=5s --timeout=5s --start-period=5s --retries=3 CMD curl -f http://0.0.0.0:5000/health || exit 1
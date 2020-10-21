# image base
FROM python:3.8.5-alpine

# nuevo
# instalando dependencias
RUN apk update && \
    apk add --virtual build-deps gcc python3-dev musl-dev && \
    apk add postgresql-dev && \
    apk add netcat-openbsd

# estableciendo direcetorio de trabajo
WORKDIR /usr/src/app

# agregando e instalando requirements
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

# nuevo
# agregando entrypoint.sh
COPY ./entrypoint.sh /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

# agregando app
COPY . /usr/src/app

# nuevo
# ejecutar server
CMD ["/usr/src/app/entrypoint.sh"]

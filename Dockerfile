FROM python:3

COPY . app
WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 8000

ENTRYPOINT [ "/bin/bash", "entrypoint.sh"]

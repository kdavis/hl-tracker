FROM python:3.8.2-alpine
LABEL maintainer="Keir Davis <keirjdavis@gmail.com>"

WORKDIR /app

COPY requirements.txt /app/

RUN pip install -r requirements.txt

COPY . /app

ENTRYPOINT ["python"]

CMD ["main.py"]

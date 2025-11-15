FROM python:3.9.6-alpine

WORKDIR /

COPY . .

RUN apk add uuidgen
RUN pip install -r requirements.txt
RUN chmod +x entrypoint.sh

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "main:app"]

ENTRYPOINT ["/entrypoint.sh"]
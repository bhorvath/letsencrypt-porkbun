FROM python:3.10-alpine
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY letsencrypt-porkbun.py .

CMD [ "/usr/local/bin/python", "/app/letsencrypt-porkbun.py" ]

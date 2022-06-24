FROM python:3.10.5-alpine3.16

RUN mkdir -p /usr/src/bot
WORKDIR /usr/src/bot

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python3", "main.py"]
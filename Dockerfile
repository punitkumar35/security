FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir flask web3 python-telegram-bot requests
EXPOSE 8080
CMD ["python", "sweeper.py"]

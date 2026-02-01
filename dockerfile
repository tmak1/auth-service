FROM python:3.9-slim

WORKDIR /auth-service

ARG PORT
ARG DEBUG_PORT

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose the app port AND the debug port
EXPOSE "${PORT}" "${DEBUG_PORT}"

CMD ["python", "main.py"]
FROM python:3.11-alpine

# Встановлюємо build-tools і повний wget
RUN apk add --no-cache wget curl bash

WORKDIR /app
COPY app.py .

RUN pip install fastapi uvicorn

EXPOSE 8000

# Надійний healthcheck
HEALTHCHECK --interval=5s --timeout=10s --start-period=5s --retries=5 \
  CMD wget -qO- http://localhost:8000/healthz || exit 1

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

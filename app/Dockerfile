FROM python:3.11-alpine

WORKDIR /app

COPY app.py .

RUN pip install fastapi uvicorn

EXPOSE 8000

HEALTHCHECK --interval=10s --timeout=2s --retries=3 CMD wget -qO- http://localhost:8000/healthz || exit 1

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
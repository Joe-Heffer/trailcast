FROM python:3.12-slim AS builder

WORKDIR /build
COPY . .
RUN pip install --no-cache-dir ".[server]"

FROM python:3.12-slim

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin/uvicorn /usr/local/bin/uvicorn

WORKDIR /app

ENV PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["uvicorn", "trailcast.server:app", "--host", "0.0.0.0", "--port", "8000"]

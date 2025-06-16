# Build stage
FROM python:3.9 as builder

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt --target /app

COPY app.py .

# Runtime stage
FROM gcr.io/distroless/python3

WORKDIR /app

COPY --from=builder /app /app

USER 1000

EXPOSE 5000

CMD ["app.py"]


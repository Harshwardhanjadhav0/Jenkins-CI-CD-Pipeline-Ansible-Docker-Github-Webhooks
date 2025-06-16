# Build stage
FROM python:3.9 as builder

WORKDIR /app

RUN pip install flask

COPY app.py .

# Runtime stage
FROM gcr.io/distroless/python3

WORKDIR /app

# Copy necessary components from builder
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY --from=builder /app/app.py .

# Run as non-root
USER 1000

EXPOSE 5000

CMD ["/usr/local/bin/python", "app.py"]


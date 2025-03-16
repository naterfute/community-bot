# Stage 1: Build
FROM python:3.13-alpine AS builder

# Install build dependencies and Inkscape
RUN apk add --no-cache \
	gcc \
	musl-dev \
	python3-dev \
	linux-headers \
	git 

# Copy application files and install Python dependencies
COPY . /app
WORKDIR /app
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt --target=/app/dependencies

# Stage 2: Final Image
FROM python:3.13-alpine

# Install runtime dependencies
RUN apk add --no-cache \
	bash \
	git 

# Copy application and dependencies
COPY --from=builder /app /app
WORKDIR /app

# Create a non-root user and switch to it
RUN adduser -D app
USER app

# Enter the Environment
ENV PYTHONPATH=/app/dependencies
# Command to run the application
CMD ["bash", "/app/run.sh"]


# ------------------------------------------------------------------------------------
# STAGE 1: BUILDER (Compiles dependencies to keep final image small)
# ------------------------------------------------------------------------------------
FROM python:3.11-slim as builder

WORKDIR /app

# Install system dependencies required for building Python packages (e.g., psycopg2)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies into a virtual environment
COPY requirements.txt .
RUN python -m venv /opt/venv
# Make sure we use the venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ------------------------------------------------------------------------------------
# STAGE 2: RUNNER (The actual production image)
# ------------------------------------------------------------------------------------
FROM python:3.11-slim as runner

WORKDIR /app

# Install runtime library for Postgres (libpq)
RUN apt-get update && apt-get install -y \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the virtual environment from the builder stage
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy the application code
COPY . .

# SECURITY: Create a non-root user
# Running as 'root' inside Docker is a security risk.
RUN addgroup --system --gid 1001 appgroup && \
    adduser --system --uid 1001 --ingroup appgroup appuser
    
# Change ownership of the app directory
RUN chown -R appuser:appgroup /app

# Switch to non-root user
USER appuser

# Set Python path so it finds 'app' module
ENV PYTHONPATH=/app

# The command to run the application
# We use a shell script to handle migrations & seeding before starting
CMD ["./start.sh"]
# ---------------------------------------------------------
# STAGE 1: BUILDER
# ---------------------------------------------------------
FROM golang:1.21-alpine AS builder

WORKDIR /app

# Install git (required for fetching Go modules)
RUN apk add --no-cache git

# Copy dependency files first (Caching layer)
COPY go.mod go.sum ./
RUN go mod download

# Copy source code
COPY . .

# Build the binary
# -ldflags="-w -s" strips debug info to reduce size
RUN CGO_ENABLED=0 GOOS=linux go build -ldflags="-w -s" -o bouncer .

# ---------------------------------------------------------
# STAGE 2: RUNNER (Production Image)
# ---------------------------------------------------------
FROM alpine:latest

WORKDIR /root/

# Install CA certificates (required for HTTPS calls if needed later)
RUN apk --no-cache add ca-certificates

# Copy binary from builder
COPY --from=builder /app/bouncer .

# Expose the WebSocket port
EXPOSE 8080

# Run the binary
CMD ["./bouncer"]
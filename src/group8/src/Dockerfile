
# Stage 1: Build the Go application
FROM golang:1.23 as builder

ENV GOPROXY=https://goproxy.cn


# Set build arguments
#ARG http_proxy=http://127.0.0.1:2081
#ARG https_proxy=http://127.0.0.1:2081

# Set environment variables for the build
#ENV http_proxy=${http_proxy}
#ENV https_proxy=${https_proxy}

# Set the working directory inside the container
WORKDIR /app

# Copy go.mod and go.sum files
COPY go.mod go.sum ./

# Download all dependencies. Dependencies will be cached if the go.mod and go.sum files are not changed
RUN go mod download

# Copy the source code into the container
COPY . .

# Build the Go application
ENV CGO_ENABLED=0 GOOS=linux GOARCH=amd64
RUN go build -o main .

# Stage 2: Create a minimal image with the compiled binary
FROM alpine:latest

# Set the working directory inside the container
WORKDIR /root/

# Copy the binary from the builder stage
COPY --from=builder /app/main .

# Copy additional files to the container
COPY --from=builder /app/trie_data.json .
COPY --from=builder /app/words.csv .

# Expose the port the application runs on
EXPOSE 8000

# Command to run the application
CMD ["./main"]

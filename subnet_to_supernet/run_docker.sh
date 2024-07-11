#!/bin/bash
# Create empty output file to ensure file exists.
touch coalesceOutput.csv

# Build the Docker image
docker build -t subnet_processor .

# Run the Docker container
docker run --rm \
  -v "$(pwd)/coalesceInput.csv:/home/tufin/coalesceInput.csv" \
  -v "$(pwd)/coalesceOutput.csv:/home/tufin/coalesceOutput.csv" \
  subnet_processor /home/tufin/coalesceInput.csv /home/tufin/coalesceOutput.csv

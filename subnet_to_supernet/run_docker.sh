#!/bin/bash

# Ensure the output file exists
touch coalesce_output.csv

# Build the Docker image
docker build -t subnet_processor .

# Run the Docker container
docker run --rm \
  -v "$(pwd)/coalesce_input.csv:/home/tufin/coalesce_input.csv" \
  -v "$(pwd)/coalesce_output.csv:/home/tufin/coalesce_output.csv" \
  subnet_processor /home/tufin/coalesce_input.csv /home/tufin/coalesce_output.csv

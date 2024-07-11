# Using small python packege
#We can run this code by running "bash run_docker.sh"
FROM python:3.10-slim

# Creating new user
RUN useradd -m tufin

# Setting working directory
WORKDIR /home/tufin

# Copying python program
COPY process_data.py .

# Install and update required packages and remove cache files
RUN apt-get update && \
    apt-get install -y --no-install-recommends && \
    rm -rf /var/lib.apt/lists/* && \
    pip install netaddr

# Switch to the new user
USER tufin

# Command to run the script
ENTRYPOINT [ "python" , "process_data.py" ]
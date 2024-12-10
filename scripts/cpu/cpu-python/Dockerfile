FROM python:latest

# Metadata
LABEL Maintainer="grozlhrle"

# Set the working directory
WORKDIR /usr/app/src

# Copy the Python script into the container
COPY az.py ./

# Install the 'stem' module
RUN pip install stem sudo

# Run the Python script
CMD ["python", "./az.py"]
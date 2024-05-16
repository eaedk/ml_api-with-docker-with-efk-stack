FROM python:3.9-slim

# Install build dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       gcc \
       python3-dev \
       build-essential \
    && rm -rf /var/lib/apt/lists/*
    
# Copy requirements file
COPY requirements.txt .

# Update pip
RUN pip install --no-cache-dir --upgrade pip

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Bundle application source
RUN mkdir /src/
COPY . /src

# set workdir
WORKDIR /src

# Expose the app's port
EXPOSE 8888

# Start application
CMD ["uvicorn","main:app", "--host", "0.0.0.0", "--port", "8888", "--reload"]
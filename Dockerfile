# Pull python base image
FROM python:3.9.6-alpine

# Set work directory
WORKDIR /usr/src/app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install dependencies
RUN pip install --upgrade pip
COPY ./pyytsync/requirements.txt .
RUN pip install -r requirements.txt

# Copy project
COPY . .

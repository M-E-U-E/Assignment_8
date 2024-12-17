# Base Image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port for PostgreSQL connection (optional)
EXPOSE 5432

# Command to run Scrapy
CMD ["scrapy", "crawl", "async_trip"]

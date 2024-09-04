FROM python:3.12

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy project files
COPY . .

# Command to run when starting the container
CMD ["python", "automated_test.py"]

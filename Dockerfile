FROM public.ecr.aws/lambda/python:3.8

# Set the working directory
WORKDIR /lambda_function

# Install the function's dependencies
COPY lambda_function/requirements.txt .
RUN pip install -r requirements.txt

# Copy the function code
COPY lambda_function/ .

# Command to run the Lambda function
CMD ["handler.lambda_handler"]

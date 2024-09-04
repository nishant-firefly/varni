
# SQS & SNS POC with FastAPI

This project is a proof of concept (POC) for working with AWS SQS and SNS using LocalStack, along with a FastAPI application for API interaction. The project includes scripts to create, send, receive, and test messages in SQS and SNS.

## File Structure

sqs_sns_poc/ │ ├── api/ │ ├── init.py # Initializes the API module │ ├── endpoints.py # Contains FastAPI route handlers for SQS/SNS services │ ├── automated_test.py # Script to automate sending and receiving different types of messages ├── create_services.py # Script to create SQS and SNS services in LocalStack ├── docker-compose.yml # Docker Compose file to set up LocalStack and FastAPI services ├── Dockerfile # Dockerfile to build the FastAPI application ├── main.py # Main script to run the FastAPI application ├── receive_message.py # Script to receive and delete messages from the SQS queue ├── send_message.py # Script to send a basic message to the SQS queue ├── send_message_json.py # Script to send a JSON message to the SQS queue ├── send_message_file_reference.py # Script to send a message containing a file reference ├── send_message_with_attributes.py # Script to send a message with attributes ├── send_message_large_payload.py # Script to send a large payload message ├── sns_notifications.py # Script to send a notification via SNS ├── requirements.txt # Python dependencies ├── README.md # This README file └── view_services.py # Script to view SQS queues and SNS topics



## Getting Started

### Prerequisites

- Docker and Docker Compose installed on your system.
- Python 3.8+ installed on your system.

### Installation

1. **Clone the repository:**

   ```sh
   git clone https://github.com/your-username/sqs_sns_poc.git
   cd sqs_sns_poc

2. **Set up a Python virtual environment:**

python -m venv myenv
source myenv/bin/activate  # On Windows use `myenv\Scripts\activate`


3. **Install the required Python packages:**


pip install -r requirements.txt


**Running the Project**

1.**Build and start the Docker containers:**

This command will set up LocalStack and FastAPI services.

     docker-compose up --build
2. **Create SQS and SNS services:**

Run this script to create SQS queues and SNS topics in LocalStack.


    python create_services.py

3. **Send and receive messages:**

Use the following scripts to send and receive different types of messages:

**Send a basic message:**

      python send_message.py

**Send a JSON message:**

      python send_message_json.py

**Send a file reference message:**

       python send_message_file_reference.py

**Send a message with attributes:**

       python send_message_with_attributes.py

**Send a large payload message:**

       python send_message_large_payload.py

**Receive and delete messages from SQS:**

        python receive_message.py

4.**View SQS and SNS services:**

Run the following script to view existing SQS queues and SNS topics:

        python view_services.py

5.**Run automated tests:**

This script will automate sending and receiving various types of messages:

        python automated_test.py
6. **Run the FastAPI application:**

The FastAPI application will be accessible at http://localhost:8001.


         python main.py

**Accessing the API**
Once the FastAPI application is running, you can access it via the following endpoints:

1. **Root Endpoint:**
     GET /
    Returns a simple JSON message.

2.**SQS/SNS Endpoints:**

    Refer to the endpoints.py file for detailed routes.


**Here is a FastAPI project, including instructions on how to test the /send-message endpoint with dynamic messages in Postman:**

# FastAPI Project with SQS & SNS Integration

## Overview

This project demonstrates a FastAPI application with endpoints for testing SQS and SNS integration. The application includes a simple `/send-message` endpoint that allows sending messages via POST requests.


## Endpoints

### 1. `/`

- **Method**: GET
- **Description**: Returns a simple "Hello, World" message.
- **Response**:
  ```json
  {
    "Hello": "World"
  }


## 2. /send-message
- **Method**: POST

-**Description**: Receives a message and returns it in the response. If no message is provided, returns "No message provided".

-**Request Body**:

-**Content-Type**: application/json

-**Body**
{
  "message": "Your dynamic message here"
}

***Response:**

## If a message is provided:

{
  "Received Message": "Your dynamic message here"
}

## If no message provided:

{
  "Message": "No message provided"
}






    
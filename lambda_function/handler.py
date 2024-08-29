import json

def lambda_handler(event, context):
    print("Received event:", json.dumps(event, indent=2))
    # Use event data for processing
    return {
        'statusCode': 200,
        'body': json.dumps(f"Received payload: {event}")
    }





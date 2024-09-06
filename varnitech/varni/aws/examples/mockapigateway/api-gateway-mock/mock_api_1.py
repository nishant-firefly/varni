import json

def lambda_handler(event, context):
    body = json.loads(event['body'])
    response = {
        "statusCode": 500,
        "body": json.dumps({
            "status": 500,
            "message": "Key not matched in API 1"
        })
    }
    
    if body.get('Id') == '9822':
        response = {
            "statusCode": 200,
            "body": json.dumps({
                "status": 200,
                "message": "Key matched in API 1"
            })
        }
    
    return response

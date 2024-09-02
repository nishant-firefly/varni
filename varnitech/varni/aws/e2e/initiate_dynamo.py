from __init__ import client_dynamodb
from botocore.exceptions import ClientError

ApiTemplates = "ApiTemplates"

def delete_and_recreate_table(table_name):
    try:
        client_dynamodb.delete_table(TableName=table_name)
        print(f"Table {table_name} deletion initiated.")
        waiter = client_dynamodb.get_waiter('table_not_exists')
        waiter.wait(TableName=table_name)
        print(f"Table {table_name} deleted.")
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            print(f"Table {table_name} does not exist.")
        else:
            print(f"Unexpected error: {e}")

    create_table(table_name)

def create_table(table_name):
    try:
        client_dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {
                    'AttributeName': 'TemplateName',
                    'KeyType': 'HASH'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'TemplateName',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        print(f"Table {table_name} creation initiated.")
        waiter = client_dynamodb.get_waiter('table_exists')
        waiter.wait(TableName=table_name)
        print(f"Table {table_name} created.")
    except ClientError as e:
        print(f"Unexpected error: {e}")

def populate_api_templates():
    try:
        client_dynamodb.put_item(
            TableName=ApiTemplates,
            Item={
                'TemplateName': {'S': 'GetUser'},
                'TemplateUrl': {'S': 'https://api.example.com/users/{}'},
                'HttpMethod': {'S': 'GET'},
                'Headers': {'M': {'Authorization': {'S': 'Bearer {}'}}},
                'BodyTemplate': {'S': ''}
            },
            ConditionExpression='attribute_not_exists(TemplateName)'
        )
        print("API Template 'GetUser' inserted.")
    except ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            print("API Template 'GetUser' already exists. Skipping insertion.")
        else:
            print(f"Unexpected error when populating templates: {e}")

def one_time_dynamo_set_up():
    delete_and_recreate_table(ApiTemplates)
    delete_and_recreate_table('ApiExecutionResults')
    populate_api_templates()
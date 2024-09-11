from service_aws import AwsService

import boto3

class DynamoDB(AwsService):
    def __init__(self):
        super().__init__("dynamodb")

    def create(self, table_name, item):
        table = boto3.resource('dynamodb').Table(table_name)
        table.put_item(Item=item)

    def read(self, table_name, key):
        table = boto3.resource('dynamodb').Table(table_name)
        response = table.get_item(Key=key)
        return response.get('Item')

    def update(self, table_name, key, update_expression, expression_attribute_values):
        table = boto3.resource('dynamodb').Table(table_name)
        table.update_item(
            Key=key,
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values
        )

    def delete(self, table_name, key):
        table = boto3.resource('dynamodb').Table(table_name)
        table.delete_item(Key=key)
        
    def list(self, table_name):
        table = boto3.resource('dynamodb').Table(table_name)
        response = table.scan()
        return response.get('Items', [])

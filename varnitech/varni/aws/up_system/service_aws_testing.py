# main.py
from service_aws_s3 import S3
from service_aws_dynamodb import DynamoDB
from service_aws_rds import RDS

if __name__ == "__main__":
    # S3 Example
    s3_service = S3()
    s3_service.create("my-bucket", "test.txt", "path/to/test.txt")
    content = s3_service.read("my-bucket", "test.txt")
    print(content)
    s3_service.update("my-bucket", "test.txt", "path/to/new_test.txt")
    s3_service.delete("my-bucket", "test.txt")
    objects = s3_service.list("my-bucket")
    print(objects)
    
    # DynamoDB Example
    dynamodb_service = DynamoDB()
    dynamodb_service.create("my-table", {"id": 1, "name": "Test Item"})
    item = dynamodb_service.read("my-table", {"id": 1})
    print(item)
    dynamodb_service.update("my-table", {"id": 1}, "set #name = :val", {"#name": "name", ":val": "Updated Item"})
    dynamodb_service.delete("my-table", {"id": 1})
    items = dynamodb_service.list("my-table")
    print(items)
    
    # RDS Example
    rds_service = RDS()
    rds_service.create("my-db-instance", "db.t2.micro", "mysql", AllocatedStorage=20, MasterUsername="admin", MasterUserPassword="password")
    instances = rds_service.read("my-db-instance")
    print(instances)
    rds_service.update("my-db-instance", AllocatedStorage=25)
    rds_service.delete("my-db-instance")
    db_instances = rds_service.list()
    print(db_instances)

import boto3
from sqlalchemy import create_engine

def upload_to_s3(file_name, bucket_name, s3_file_name, aws_access_key, aws_secret_key):
    s3 = boto3.client(
        's3',
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key
    )
    
    try:
        s3.upload_file(file_name, bucket_name, s3_file_name)
        print(f"{file_name} uploaded to {bucket_name}/{s3_file_name}")
    except Exception as e:
        print(f"Error uploading to S3: {str(e)}")

def get_postgres_engine(user, password, host, db):
    db_url = f'postgresql://{user}:{password}@{host}/{db}'
    engine = create_engine(db_url)
    return engine

if __name__ == "__main__":
    # Example usage for uploading a file to S3
    upload_to_s3('data/tips.csv', 'my-bucket', 'tips.csv', 'my_aws_access_key', 'my_aws_secret_key')

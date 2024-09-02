from service_aws import AwsService

class S3(AwsService):
    def __init__(self):
        # self.boto_client will be initiated 
        super().__init__("s3")
    
    def create(self, bucket_name, object_name, file_path):
        self.boto_client.upload_file(file_path, bucket_name, object_name)

    def read(self, bucket_name, object_name):
        response = self.boto_client.get_object(Bucket=bucket_name, Key=object_name)
        return response['Body'].read()

    def update(self, bucket_name, object_name, file_path):
        self.create(bucket_name, object_name, file_path)  # Overwrite the object

    def delete(self, bucket_name, object_name):
        self.boto_client.delete_object(Bucket=bucket_name, Key=object_name)
        
    def list(self, bucket_name):
        response = self.boto_client.list_objects_v2(Bucket=bucket_name)
        return response.get('Contents', [])

if __name__=="__main__":
    s3=S3()
    print(s3.client)
    breakpoint()



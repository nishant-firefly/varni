from service_aws import AwsService

class RDS(AwsService):
    def __init__(self):
        super().__init__("rds")

    def create(self, db_instance_identifier, db_instance_class, engine, **kwargs):
        self.boto_client.create_db_instance(
            DBInstanceIdentifier=db_instance_identifier,
            DBInstanceClass=db_instance_class,
            Engine=engine,
            **kwargs
        )

    def read(self, db_instance_identifier):
        response = self.boto_client.describe_db_instances(DBInstanceIdentifier=db_instance_identifier)
        return response['DBInstances']

    def update(self, db_instance_identifier, **kwargs):
        self.boto_client.modify_db_instance(DBInstanceIdentifier=db_instance_identifier, **kwargs)

    def delete(self, db_instance_identifier, skip_final_snapshot=True, **kwargs):
        self.boto_client.delete_db_instance(
            DBInstanceIdentifier=db_instance_identifier,
            SkipFinalSnapshot=skip_final_snapshot,
            **kwargs
        )

    def list(self):
        response = self.boto_client.describe_db_instances()
        return response['DBInstances']

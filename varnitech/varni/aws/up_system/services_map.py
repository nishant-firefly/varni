from service_localstack_docker import LocalstackService, DockerService
from enum import Enum
class ServiceConst(Enum):
    Docker="Docker"
    Localstack="Localstack"

SERVICES_MAP={
                ServiceConst.Docker.value: DockerService,
                ServiceConst.Localstack.value:LocalstackService
                # Add more services here
}
DOCKER_LOCALSTACK=[
    ServiceConst.Docker.value, 
    ServiceConst.Localstack.value, 
]
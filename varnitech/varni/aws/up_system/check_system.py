from utils import CheckService
from services_map import DOCKER_LOCALSTACK

def CheckDockerLocalstack():
    return CheckService(DOCKER_LOCALSTACK).check_service()

if __name__=="__main__":
    print(CheckDockerLocalstack())


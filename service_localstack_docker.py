import docker
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class LocalstackServiceStatus:
    def __init__(self, container_name):
        self.container_name = container_name
        self.docker_client = docker.from_env()

    def check_container_status(self):
        try:
            container = self.docker_client.containers.get(self.container_name)
            if container.status == "running":
                print(f"Container '{self.container_name}' is running.")
            else:
                print(f"Container '{self.container_name}' is not running (status: {container.status}).")
        except docker.errors.NotFound:
            print(f"Container '{self.container_name}' not found.")

if __name__ == "__main__":
    container_name = 'localstack_main'  # Ensure this matches your Docker container name
    localstack_status = LocalstackServiceStatus(container_name)
    localstack_status.check_container_status()

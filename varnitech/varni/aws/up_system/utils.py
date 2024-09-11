import traceback
from enum import Enum
from abc import abstractmethod, ABC
from __init__ import pdm # TODO:  Move to utils
import json
import os

CONFIG_FILE = 'config.json'
ENV_FILE = '.env'

class RunningStatus:
    RUNNING, EXCEPTION, MESSAGE, TRACEBACK = "running", "exception", "message", "traceback"

    def __init__(self, running: bool, e: Exception = None, message: str = None) -> None:
        self.running = running
        self.exception = str(e) if e else None
        self.message = message
        self.traceback = traceback.format_exc() if e else None

    def __repr__(self) -> str:

        return str(dict(self))

    def __str__(self) -> str:
        return str(dict(self))

    def to_dict(self) -> dict:
        loc_dict=dict(self)
        if loc_dict['running']==True:
            # If status running do not show None messages, exceptions etc.
            return {k:v for k,v in loc_dict.items() if v}
        return loc_dict

    def __iter__(self):
        yield RunningStatus.RUNNING, self.running
        yield RunningStatus.EXCEPTION, self.exception
        yield RunningStatus.MESSAGE, self.message
        yield RunningStatus.TRACEBACK, self.traceback
class Service(ABC):
    @abstractmethod
    def check(self) -> RunningStatus:
        pass
class CheckService:
    
    EXC_MSG_DEFENSIVE_CODE_FOR_SERVICE= "Defensive Coding: caught in generic exception while checking {}"

    def __init__(self, SERVICES_LIST) -> None:
        # TODO: Move out and resolve cyclic import error.
        from services_map import SERVICES_MAP
        self.services_check_map={k:v for k,v in SERVICES_MAP.items() if k in SERVICES_LIST}


    class ServiceStatusMessage(Enum):
        SERVICE_NOT_RUNNING = "{} is not running!"
        SERVICE_RUNNING = "{} is running!"

    def check_service(self) -> dict:

        statuses = {name: getattr(service_class(),'check')() for name, service_class in self.services_check_map.items()}
        for service_name, status in statuses.items():
            if not status.running:
                pdm(CheckService.ServiceStatusMessage.SERVICE_NOT_RUNNING.value.format(service_name))
            else:
                pdm(CheckService.ServiceStatusMessage.SERVICE_RUNNING.value.format(service_name))
        return {service_name: status.to_dict() for service_name, status in statuses.items()}


ENV_STRS = {
    # EnvFileManager
    'file_not_found': "Error: The file {filename} does not exist.",
    'invalid_json': "Error: The file {filename} is not a valid JSON.",
    'added_settings': "Added settings:",
    'deleted_settings': "Deleted settings:",
    'modified_settings': "Modified settings:",
    'update_prompt': "Do you want to update the .env file? (y/n): ",
    'write_success': ".env file updated successfully.",
    'write_error': "Error: Could not write to {filename}.",
    'no_changes': "No changes detected. No update needed.",
    'update_canceled': "Update canceled by the user.",

    # AWSCredentialsGenerator
    'aws_key_generated': "AWS Access Key and Secret Key generated.",
    "AKIA":"AKIA",
    "AWS_ACCESS_KEY_ID":"AWS_ACCESS_KEY_ID",
    "AWS_SECRET_ACCESS_KEY":"AWS_SECRET_ACCESS_KEY"

}    
class EnvFileManager:
    def __init__(self, json_file, env_file):
        self.json_file = json_file
        self.env_file = env_file

    def read_json(self):
        """Reads the JSON file and returns a dictionary of the configuration."""
        try:
            with open(self.json_file, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            print(ENV_STRS['file_not_found'].format(filename=self.json_file))
            return None
        except json.JSONDecodeError:
            print(ENV_STRS['invalid_json'].format(filename=self.json_file))
            return None

    def read_env(self):
        """Reads the .env file and returns a dictionary of the configuration."""
        if not os.path.exists(self.env_file):
            return {}
        with open(self.env_file, 'r') as file:
            return {line.split('=')[0]: line.split('=')[1].strip() for line in file if '=' in line}

    def write_env(self, config):
        """Writes the configuration to a .env file after checking for changes."""
        current_config = self.read_env()
        config = {**current_config, **config}  # Merge new config with existing
        try:
            with open(self.env_file, 'w') as file:
                for key, value in config.items():
                    file.write(f'{key}={value}\n')
            print(ENV_STRS['write_success'])
        except IOError:
            print(ENV_STRS['write_error'].format(filename=self.env_file))



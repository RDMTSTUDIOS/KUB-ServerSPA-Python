from os import path
import yaml

class KUBServerConfigLoaderException_MissingConfigFile(Exception):
    def __init__(self, path: str, *args: object) -> None:
        super().__init__(*args, f'Config on specified path {path} does not exist')

class KUBServerConfigLoaderException_MissingValue(Exception):
    def __init__(self, fields: list[str], *args: object) -> None:
        super().__init__(*args, f'Config missing essential fields:\n{fields}')


# @description(Yaml config-file loader for server setup)
# @return(dict[str, str | int])
# @raisable
# @sure(
#   - config.yaml file exists;
#   - config contains essential values and values type matches excepted;
# )
def server_config_loader(config_file_path: str = './config.yaml') -> dict[str, str | int]:
    if not path.isfile(config_file_path):
        raise KUBServerConfigLoaderException_MissingConfigFile(config_file_path)
    
    ESSENTIAL_VALUES: list[str] = ['HOST', 'PORT']

    with open(config_file_path, 'r') as config_file:

        MISSING_FIELDS: list[str] = []

        config: dict = yaml.safe_load(config_file)
        for essential_value in ESSENTIAL_VALUES:
            if not config.get(essential_value, None):
                MISSING_FIELDS.append(essential_value)

        if not not len(MISSING_FIELDS):
            raise KUBServerConfigLoaderException_MissingValue(essential_value)
        
        return config
import yaml


class Config:
    YAML_EXTENSION: str = "yaml"
    YML_EXTENSION: str = "yml"
    DEFAULT_FILE_PATH: str = "config.yml"
    
    def __init__(self, file_path=None):
        if file_path is None:
            self.file_path = Config.DEFAULT_FILE_PATH
        else:
            self.file_path = file_path
        self.config_data = self.load_config(file_path)

    def load_config(self, file_path):
        if (
            not self.check_extension(Config.YAML_EXTENSION) or 
            not self.check_extension(Config.YML_EXTENSION)
        ):
            raise Exception(f"Not a yaml file: {file_path}")
        
        try:
            with open(file_path, 'r') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f'Config file not found at: {file_path}')
        except yaml.YAMLError as e:
            raise ValueError(f'Error while parsing YAML file: {e}')

    def get(self, key):
        return self.config_data.get(key)

    def set(self, key, value):
        self.config_data[key] = value
        self.save_to_file(self.file_path)

    def save_to_file(self, file_path):
        with open(file_path, 'w') as file:
            yaml.dump(self.config_data, file, default_flow_style=False)

    def check_extension(self, expected_extension):
        if not isinstance(expected_extension, str):
            raise ValueError("Expected extension must be a string.")
        
        actual_extension = self.file_path.split('.')[-1]
        return actual_extension == expected_extension


config = Config('config.yaml')

api_key = config.get('api_key')
base_url = config.get('base_url')

import yaml
import os

class Config:
    YAML_EXTENSION: str = "yaml"
    YML_EXTENSION: str = "yml"
    
    _ROOT_DIR: str = os.path.dirname(os.path.dirname(__file__))
    DEFAULT_FILE_PATH: str = os.path.join(_ROOT_DIR, "config.yml")
    
    def __init__(self, file_path=None):
        if file_path is None:
            self.file_path = Config.DEFAULT_FILE_PATH
        else:
            self.file_path = file_path
        self.config_data = self.load_config()

    def load_config(self):
        if (
            not self.check_extension(Config.YAML_EXTENSION) and 
            not self.check_extension(Config.YML_EXTENSION)
        ):
            raise Exception(f"Not a yaml file: {self.file_path}")
        
        try:
            with open(self.file_path, 'r') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f'Config file not found at: {self.file_path}')
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


config = Config()

schema1 = config.get('Compare')
schema2 = config.get('schema2')
print(schema1)
print(schema2)
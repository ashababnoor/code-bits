import yaml
import os
from dataclasses import dataclass
from typing import Dict, Any, Tuple


@dataclass
class Table:
    project_id: str
    dataset_id: str
    table_id: str
    
    @staticmethod
    def get_tables_from_config(config_key: str, config_file_path: str = None) -> Tuple['Table']:
        config = Config(file_path=config_file_path)
        return config.get_tables(config_key)


class Config:
    YAML_EXTENSION: str = "yaml"
    YML_EXTENSION: str = "yml"
    
    _ROOT_DIR: str = os.path.dirname(os.path.dirname(__file__))
    DEFAULT_FILE_PATH: str = os.path.join(_ROOT_DIR, "config.yml")
    
    def __init__(self, file_path: str = None):
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

    def get(self, key: str):
        return self.config_data.get(key)
    
    def get_tables(self, key: str) -> Tuple[Table]:
        table_pair = self.get(key)
        table1 = table_pair.get('table1')
        table2 = table_pair.get('table2')
        if table1 is None or table2 is None:
            raise Exception("Key for table information not found! Check demo_config.yml for format.")
        
        return Table(**table1), Table(**table2)

    def set(self, key: str, value: Any) -> None:
        self.config_data[key] = value
        self.save_to_file(self.file_path)

    def save_to_file(self, file_path) -> None:
        with open(file_path, 'w') as file:
            yaml.dump(self.config_data, file, default_flow_style=False)

    def check_extension(self, expected_extension: str) -> bool:
        if not isinstance(expected_extension, str):
            raise ValueError("Expected extension must be a string.")
        
        actual_extension = self.file_path.split('.')[-1]
        return actual_extension == expected_extension


def main():
    config_key = "food_tables"
    table1, table2 = Table.get_tables_from_config(config_key)
    
    print(f"{table1 = }")
    print(f"{table2 = }")
    
if __name__ == "__main__":
    main()
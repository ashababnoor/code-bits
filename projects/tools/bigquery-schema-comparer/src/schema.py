from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class Table:
    project_id: str
    dataset_id: str
    table_id: str
    schema: Dict[str, Any]
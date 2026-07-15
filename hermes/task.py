from dataclasses import dataclass, field
from typing import Any
import uuid

@dataclass
class Task:
    type: str                        # what kind of task eg. "scrape_ads"
    payload: dict = field(default_factory=dict)   # input data
    result: dict = field(default_factory=dict)    # output data
    status: str = "todo"             # todo → in_progress → done → failed
    agent: str = ""                  # which agent owns this task
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])  # short unique id

    def __repr__(self):
        return f"Task(id={self.id}, type={self.type}, status={self.status})"
from abc import abstractmethod
from typing import Optional

from obj import Joint, Skeleton

class Parser:
    def __init__(self):
        self.parsed_file: Optional[str] = None
        self.changed: bool = False
        self.parsed_skeleton: Optional[Skeleton] = None
        

    @abstractmethod
    def parse_file(self, filepath: str) -> Joint:
        pass

    def save_change(self) -> None:
        self.save_as(self, self.parsed_file)

    @abstractmethod
    def save_as(self, filepath: str) -> None:
        pass
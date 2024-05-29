from abc import ABC, abstractmethod
from typing import Any, List

class OutputType(ABC):
    @abstractmethod
    def get_output(self, path: List[str], distance: int) -> Any:
        pass


class Route(OutputType):
    def get_output(self, path: List[str], distance: int) -> List[str]:
        return path


class Distance(OutputType):
    def get_output(self, path: List[str], distance: int) -> int:
        return distance

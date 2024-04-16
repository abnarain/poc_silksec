from abc import ABC, abstractmethod
class DataFetcher(ABC):
    @abstractmethod
    def fetch_json(self):
        pass

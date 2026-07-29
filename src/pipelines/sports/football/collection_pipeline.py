from abc import abstractmethod
from collections.abc import Iterable

from pipelines.sports.football.base_pipeline import BasePipeline


class CollectionPipeline(BasePipeline):

    @abstractmethod
    def get_work_items(self) -> Iterable:
        pass

    @abstractmethod
    def extract(self, item):
        pass

    def transform(self, data):
        return data

    @abstractmethod
    def load(self, data, item):
        pass

    def run(self):
        for index, item in enumerate(self.get_work_items(), start=1):
            print(f"[{index}] Processing {item}")

            data = self.extract(item)
            data = self.transform(data)
            self.load(data, item)
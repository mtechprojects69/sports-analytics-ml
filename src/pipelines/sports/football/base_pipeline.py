from abc import ABC, abstractmethod


class BasePipeline(ABC):

    @abstractmethod
    def extract(self):
        pass

    @abstractmethod
    def transform(self, data):
        pass

    @abstractmethod
    def load(self, data):
        pass

    def run(self):
        data = self.extract()
        data = self.transform(data)
        return self.load(data)
from __future__ import annotations

import os
import time
from threading import Thread
from typing import List, Iterator, Type
from tempfile import TemporaryDirectory


class GenericInputData:
    def __init__(self, path: str, *args, **kwargs):
        self.path = path

    def read(self):
        raise NotImplementedError

    @classmethod
    def generate_inputs(cls, config: dict) -> Iterator[GenericInputData]:
        data_dir = config["data_dir"]
        for name in os.listdir(data_dir):
            yield cls(os.path.join(data_dir, name))


class PathInputData(GenericInputData):
    def read(self):
        return open(self.path).read()


class GenericWorker:
    def __init__(self, input_data: GenericInputData):
        self.input_data = input_data
        self.result = 0

    def map(self):
        raise NotImplementedError

    def reduce(self, other: GenericWorker):
        raise NotImplementedError

    @classmethod
    def create_workers(
        cls, input_class: Type[GenericInputData], config: dict
    ) -> List[GenericWorker]:
        workers = []
        for input_data in input_class.generate_inputs(config):
            workers.append(cls(input_data))
        return workers


class LineCountWorker(GenericWorker):
    def map(self):
        data = self.input_data.read()
        self.result = data.count("\n")

    def reduce(self, other: GenericWorker):
        self.result += other.result


def execute(workers: List[GenericWorker]) -> int:
    threads = [Thread(target=w.map) for w in workers]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    first, rest = workers[0], workers[1:]
    for worker in rest:
        first.reduce(worker)
    return first.result


def mapreduce(
    worker_class: Type[GenericWorker],
    input_class: Type[GenericInputData],
    config: dict,
):
    workers = worker_class.create_workers(input_class, config)
    return execute(workers)


def write_test_files(temp_dir: str):
    with open(os.path.join(temp_dir, "test_1.txt"), "w") as f:
        f.write("qwe\nqwe\n")
    with open(os.path.join(temp_dir, "test_2.txt"), "w") as f:
        f.write("qwe\nqwe\n")
    with open(os.path.join(temp_dir, "test_3.txt"), "w") as f:
        f.write("qwe\nqwe\n")


if __name__ == "__main__":
    with TemporaryDirectory() as temp_dir:
        write_test_files(temp_dir)
        config = {"data_dir": temp_dir}
        result = mapreduce(LineCountWorker, PathInputData, config)

    print(f"result: {result}")

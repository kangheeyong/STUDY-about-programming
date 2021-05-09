from __future__ import annotations

import os
import time
from threading import Thread
from typing import List, Iterator
from tempfile import TemporaryDirectory


class InputData:
    def read(self):
        raise NotImplementedError


class PathInputData(InputData):
    def __init__(self, path: str):
        super().__init__()
        self.path = path

    def read(self):
        return open(self.path).read()


class Worker:
    def __init__(self, input_data: InputData):
        self.input_data = input_data
        self.result = 0

    def map(self):
        raise NotImplementedError

    def reduce(self, other: Worker):
        raise NotImplementedError


class LineCountWorker(Worker):
    def map(self):
        data = self.input_data.read()
        self.result = data.count("\n")

    def reduce(self, other: Worker):
        self.result += other.result


def generate_inputs(data_dir: str) -> Iterator[PathInputData]:
    for name in os.listdir(data_dir):
        yield PathInputData(os.path.join(data_dir, name))


def create_workers(input_list: Iterator[PathInputData]) -> List[LineCountWorker]:
    workers = []
    for input_data in input_list:
        workers.append(LineCountWorker(input_data))
    return workers


def execute(workers: List[LineCountWorker]) -> int:
    threads = [Thread(target=w.map) for w in workers]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    first, rest = workers[0], workers[1:]
    for worker in rest:
        first.reduce(worker)
    return first.result


def mapreduce(data_dir: str):
    inputs = generate_inputs(data_dir)
    workers = create_workers(inputs)
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
        result = mapreduce(temp_dir)

    print(f"result: {result}")

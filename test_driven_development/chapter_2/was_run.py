from __future__ import annotations

from typing import List


class TestCase:
    def __init__(self, name: str):
        self.name = name

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def run(self, result: TestResult):
        result.testStarted()
        self.setUp()
        try:
            method = getattr(self, self.name)
            method()
        except:
            result.testFailed()
        self.tearDown()
        return result


class TestResult:
    def __init__(self):
        self.runCount = 0
        self.failureCount = 0

    def testStarted(self):
        self.runCount += 1

    def testFailed(self):
        self.failureCount += 1

    def summary(self):
        return f"{self.runCount} run, {self.failureCount} failed"


class TestSuite:
    def __init__(self):
        self.tests: List[WasRun] = []

    def add(self, test: WasRun):
        self.tests.append(test)

    def run(self, result: TestResult):
        for test in self.tests:
            test.run(result)
        return result


class WasRun(TestCase):
    def __init__(self, name: str):
        super().__init__(name)

    def setUp(self):
        self.wasRun = None
        self.wasSetUp = 1
        self.log = "setUp "

    def testMethod(self):
        self.wasRun = 1
        self.log += "testMethod "

    def testBrokenMethod(self):
        raise Exception

    def tearDown(self):
        self.log += "tearDown "

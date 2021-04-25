from __future__ import annotations

import mock
import unittest
from typing import Tuple, List, Any, Type
from contextlib import contextmanager


@contextmanager
def _steal_object(target: Type[object]):
    def _call_side_effect(obj: object, *args: Any, **kwargs: Any):
        _mock.temp_original(obj, *args, **kwargs)
        _objs.append(obj)

    _objs: List[object] = []
    _mock = mock.patch.object(target, "__init__", new=_call_side_effect)
    with _mock:
        yield _objs


class TestCase(unittest.TestCase):
    def test_base(self):
        class Bar:
            def __init__(self, a: int):
                self.a = a

        def foo() -> Tuple[Bar, Bar]:
            a = Bar(1)
            b = Bar(2)
            return a, b

        with _steal_object(Bar) as objs:
            a, b = foo()

            self.assertEqual(2, len(objs))
            self.assertEqual(Bar, type(objs[0]))
            self.assertEqual(a, objs[0])
            self.assertEqual(1, objs[0].a)
            self.assertEqual(Bar, type(objs[1]))
            self.assertEqual(b, objs[1])
            self.assertEqual(2, objs[1].a)


if __name__ == "__main__":
    unittest.main()
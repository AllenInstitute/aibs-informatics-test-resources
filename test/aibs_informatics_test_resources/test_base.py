from pathlib import Path


def test__BaseTest__tmp_path__works():
    from aibs_informatics_test_resources.base import BaseTest

    class DummyTest(BaseTest):
        def test__tmp_path__works(self):
            path = self.tmp_path()
            self.assertIsInstance(path, Path)

    test_case = DummyTest("test__tmp_path__works")
    test_case.run()

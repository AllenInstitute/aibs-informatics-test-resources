import os
from pathlib import Path
from typing import ClassVar

from aibs_informatics_test_resources.base import BaseTest


class TmpPathsTest(BaseTest):
    def test__tmp_path__works(self):
        path = self.tmp_path()
        self.assertIsInstance(path, Path)
        assert path.is_dir()

    def test__tmp_file__works(self):
        path = self.tmp_file(basename="test.txt", content="test content")
        self.assertIsInstance(path, Path)
        self.assertTrue(path.exists())
        assert path.read_text() == "test content"

    def test__tmp_file__not_content__does_not_create_file(self):
        path = self.tmp_file()
        self.assertIsInstance(path, Path)
        self.assertFalse(path.exists())


class ResetEnvironTest(BaseTest):
    reset_environ: ClassVar[bool] = True

    def setUp(self) -> None:
        os.environ["TEST_ENV_VAR"] = "original_value"
        super().setUp()

    def tearDown(self) -> None:
        super().tearDown()
        assert os.environ["TEST_ENV_VAR"] == "original_value"

    def test__set_env_vars__removes_value(self):
        assert "TEST_ENV_VAR" in os.environ
        self.set_env_vars(("TEST_ENV_VAR", None))
        assert "TEST_ENV_VAR" not in os.environ

    def test__set_env_vars__updates_value(self):
        assert "TEST_ENV_VAR" in os.environ and os.environ["TEST_ENV_VAR"] == "original_value"
        self.set_env_vars(("TEST_ENV_VAR", "updated_value"))
        assert "TEST_ENV_VAR" in os.environ and os.environ["TEST_ENV_VAR"] == "updated_value"


class AssertionMethodsTest(BaseTest):
    def test__assertStringPattern__works(self):
        self.assertStringPattern(r"^\d{3}$", "123")
        with self.assertRaises(AssertionError):
            self.assertStringPattern(r"^\d{3}$", "1234")

    def test__assertJsonEqual__works(self):
        self.assertJsonEqual({"a": 1, "b": 2}, {"b": 2, "a": 1})
        with self.assertRaises(AssertionError):
            self.assertJsonEqual({"a": 1}, {"a": 2})

    def test__assertListEqual__works(self):
        self.assertListEqual([1, 2, 3], [1, 2, 3])
        with self.assertRaises(AssertionError):
            self.assertListEqual([1, 2, 3], [1, 2, 4])

    def test__assertListEquals__presorts_when_required(self):
        self.assertListEqual([1, 2, 3], [3, 2, 1], presort=True)
        with self.assertRaises(AssertionError):
            self.assertListEqual([1, 2, 3], [3, 2, 1], presort=False)


class PatchingTests(BaseTest):
    def test__no_patching__works(self):
        from test.aibs_informatics_test_resources.examples import sum

        assert sum(2, 2) == 4

    def test__patching__works(self):
        mock_sum = self.create_patch("test.aibs_informatics_test_resources.examples.sum")
        mock_sum.return_value = 5
        assert mock_sum(2, 2) == 5

    def test__chdir__works(self):
        cwd = os.getcwd()

        path = self.tmp_path()
        assert path != cwd
        with self.chdir(path):
            assert os.getcwd() == str(path)
        assert os.getcwd() != str(self.tmp_path())
        assert os.getcwd() == cwd

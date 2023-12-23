import json
import os
import re
import tempfile
import unittest
from contextlib import contextmanager
from contextlib import nullcontext as does_not_raise
from copy import deepcopy
from pathlib import Path
from typing import Any, Callable, ClassVar, List, Optional, Tuple, Union, cast
from unittest.mock import MagicMock, patch

import pytest


class BaseTest(unittest.TestCase):
    reset_environ: ClassVar[bool] = False

    def setUp(self) -> None:
        super().setUp()
        self._environ_before = deepcopy(os.environ) if self.reset_environ else None
        self._monkey_patch = pytest.MonkeyPatch()

    def tearDown(self) -> None:
        super().tearDown()
        self._monkey_patch.undo()
        if self.reset_environ and self._environ_before:
            os.environ.clear()
            os.environ.update(self._environ_before)

    @pytest.fixture(autouse=True)
    def _tmp_path_factory_class(self, tmp_path_factory):
        # set a class attribute on the invoking test context
        self._tmp_path_factory = tmp_path_factory

    def tmp_path(self, basename: Optional[str] = None) -> Path:
        return self._tmp_path_factory.mktemp(basename or self.__class__.__name__)  # type: ignore

    def tmp_file(
        self,
        basename: Optional[str] = None,
        dirname: Optional[str] = None,
        content: Optional[str] = None,
    ) -> Path:
        path = self.tmp_path(dirname) / (basename or tempfile.mktemp())
        if content:
            path.write_text(content)
        return path

    def set_env_vars(self, *key_values_pairs: Tuple[str, Optional[str]]):
        for env_key, env_value in key_values_pairs:
            if env_value:
                self._monkey_patch.setenv(env_key, env_value)
            else:
                self._monkey_patch.delenv(env_key, raising=False)

    def assertStringPattern(self, pattern: str, actual: str):
        if not re.compile(pattern).match(actual):
            raise AssertionError(f'String "{actual}" does not match pattern "{pattern}"')

    def assertJsonEqual(
        self, first: Union[dict, str, int, list], second: Union[dict, str, int, list]
    ):
        first_data = json.dumps(first, sort_keys=True)
        second_data = json.dumps(second, sort_keys=True)
        self.assertEqual(first_data, second_data)

    def assertListEqual(
        self,
        list1: List[Any],
        list2: List[Any],
        msg: Any = None,
        presort: bool = False,
        **presort_kwargs,
    ) -> None:
        return super().assertListEqual(
            sorted(list1, **presort_kwargs) if presort else list1,
            sorted(list2, **presort_kwargs) if presort else list2,
            msg,
        )

    def create_patch(self, name: str, **kwargs) -> MagicMock:
        patcher = patch(name, **kwargs)
        self.addCleanup(patcher.stop)
        thing = patcher.start()
        return thing

    @contextmanager
    def chdir(self, destination: Union[str, Path]):
        current_dir = os.getcwd()
        try:
            os.chdir(destination)
            yield
        finally:
            os.chdir(current_dir)

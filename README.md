# AIBS Informatics Test Resources

[![Build Status](https://github.com/AllenInstitute/aibs-informatics-test-resources/actions/workflows/build.yml/badge.svg)](https://github.com/AllenInstitute/aibs-informatics-test-resources/actions/workflows/build.yml)
[![codecov](https://codecov.io/gh/AllenInstitute/aibs-informatics-test-resources/graph/badge.svg?token=GY50BJBO9K)](https://codecov.io/gh/AllenInstitute/aibs-informatics-test-resources)
---

## Overview

This package provides a collection of utilities and resources to facilitate testing in various AIBS Informatics projects. It includes base test classes, mock utilities, and other helpful tools.

## Available Modules

### Base Test Class

The [`BaseTest`](./src/aibs_informatics_test_resources/base.py) class provides a base class for creating unit tests with common setup and teardown functionality. It includes the following features:

- **Environment Management**:
  - `set_env_vars(*key_values_pairs: Tuple[str, Optional[str]])`: Set environment variables for the duration of the test.
  - `reset_environ`: Class variable to reset environment variables after each test.

- **Temporary Files and Directories**:
  - `tmp_path(basename: Optional[str] = None) -> Path`: Create a temporary directory.
  - `tmp_file(basename: Optional[str] = None, dirname: Optional[str] = None, content: Optional[str] = None) -> Path`: Create a temporary file with optional content.

- **Assertions**:
  - `assertStringPattern(pattern: str, actual: str)`: Assert that a string matches a given regex pattern.
  - `assertJsonEqual(first: Union[dict, str, int, list], second: Union[dict, str, int, list])`: Assert that two JSON objects are equal.
  - `assertListEqual(list1: List[Any], list2: List[Any], msg: Any = None, presort: bool = False, **presort_kwargs) -> None`: Assert that two lists are equal, with an option to sort them before comparison.

- **Mocking**:
  - `create_patch(name: str, **kwargs) -> MagicMock`: Create a patch for a given name and add it to the cleanup list.

- **Context Managers**:
  - `chdir(destination: Union[str, Path])`: Context manager to change the current working directory temporarily.


### Mock Utilities

- `does_not_raise`: A context manager for assertions that no exceptions are raised.
- [`reset_environ_after_test`](./src/aibs_informatics_test_resources/utils.py): A decorator to reset environment variables after a test.

### Example Usage

Here is an example of how to use the `BaseTest` class in your tests:

```python
from aibs_informatics_test_resources import BaseTest

class MyTest(BaseTest):
    def test_example(self):
        self.assertEqual(1 + 1, 2)
    
    def test_use_temp_file(self):
        with self.tmp_file(content="Hello, World!") as tmp_file:
            self.assertTrue(tmp_file.exists())
            self.assertEqual(tmp_file.read_text(), "Hello, World!")

```

## Contributing
Any and all PRs are welcome. Please see [CONTRIBUTING.md](CONTRIBUTING.md) for more information.

## Licensing
This software is licensed under the Allen Institute Software License, which is the 2-clause BSD license plus a third clause that prohibits redistribution and use for commercial purposes without further permission. For more information, please visit [Allen Institute Terms of Use](https://alleninstitute.org/terms-of-use/).

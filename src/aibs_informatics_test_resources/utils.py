import functools
import os
from copy import deepcopy


def reset_environ_after_test(func):
    @functools.wraps(func)
    def wrapper_reset_environ(*args, **kwargs):
        environ_before = deepcopy(os.environ)
        try:
            return func(*args, **kwargs)
        finally:
            os.environ.clear()
            os.environ.update(environ_before)

    return wrapper_reset_environ

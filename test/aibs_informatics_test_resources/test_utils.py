def test__reset_environ_after_test__works():
    import os

    from aibs_informatics_test_resources.utils import reset_environ_after_test

    os.environ["TEST_ENV_VAR"] = "original_value"

    @reset_environ_after_test
    def test_func():
        assert os.environ["TEST_ENV_VAR"] == "original_value"
        os.environ["TEST_ENV_VAR"] = "updated_value"
        assert os.environ["TEST_ENV_VAR"] == "updated_value"

    test_func()
    assert os.environ["TEST_ENV_VAR"] == "original_value"

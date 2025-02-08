import os

import pytest
@pytest.fixture(scope="session")
def tests_base_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return current_dir


@pytest.fixture(scope="session")
def project_base_path(tests_base_path):
    project_base_path = os.path.dirname(tests_base_path)
    return project_base_path

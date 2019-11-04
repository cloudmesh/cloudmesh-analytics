"""The configuration for tests
The config is required by the pytest. The pytest will run this file at first.
"""

import os
import tempfile
import pytest
import sys

from cloudmesh.analytics.server.server import create_app
from cloudmesh.analytics.server.db import get_db, init_db

@pytest.fixture
def app():
    """Configure the flask app for testing

    This is a pytest fixture

    Attention:
        The the database is in progress, and not used. All files are saved in the folder defined in the 'UPLOAD_FOLDER'
        in the app configurations

    Warning:
        The uploaded folder is relative to where the pytest is called. Calling pytest in other folder will result a mis-
        placed uploaded folder. The uploaded folder should be kept under test directory
    """
    db_fd, db_path = tempfile.mkstemp()
    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
        # Set the folder path for testing. All uploaded files will be saved here
        'UPLOAD_FOLDER': './tests/test_upload_folder'
    })

    with app.app_context():
        init_db()

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    """The test client for simulating requests

    Return:
        Return a test client
    """
    return app.test_client()


@pytest.fixture
def runner(app):
    """
    Attention:
        Not used now
    """
    return app.test_cli_runner()
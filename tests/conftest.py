import os
import tempfile
import pytest
import sys

from cloudmesh.analytics.server.server import create_app
from cloudmesh.analytics.server.db import get_db, init_db


@pytest.fixture
def app():
    print(sys.path)
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
        # Set the folder path for testing. All uploaded files will be saved here
        'UPLOAD_FOLDER': './testing_files'
    })

    with app.app_context():
        init_db()

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
import pytest

from app import create_app, db as _db


@pytest.yield_fixture(scope='session')
def app(request):
    app = create_app()

    # Config overrides
    app.config['TESTING'] = True
    app.config['SQL_ALCHEMY_DATABASE_URI'] = 'sqlite:///'
    app.config['SERVER_NAME'] = 'http://localhost:5000/'

    ctx = app.app_context()
    ctx.push()

    yield app

    ctx.pop()


@pytest.yield_fixture(scope='function')
def db(app, request):
    _db.app = app
    _db.create_all()

    yield _db

    _db.drop_all()

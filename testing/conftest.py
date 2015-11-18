import pytest

from app import create_app, db as _db


@pytest.yield_fixture(scope='session', autouse=True)
def app(request):
    app = create_app()

    # Config overrides
    app.config['TESTING'] = True
    app.config['SQL_ALCHEMY_DATABASE_URI'] = 'sqlite:///'

    ctx = app.test_request_context()
    ctx.push()

    yield app

    ctx.pop()


@pytest.yield_fixture(scope='session', autouse=True)
def db(app, request):
    _db.app = app
    _db.create_all()

    yield _db

    _db.drop_all()


@pytest.fixture(autouse=True)
def db_session(request, monkeypatch, db):
    # Roll back at the end of every test
    request.addfinalizer(db.session.remove)

    # Prevent the session from closing (make it a no-op) and
    # committing (redirect to flush() instead)
    monkeypatch.setattr(db.session, 'commit', db.session.flush)
    monkeypatch.setattr(db.session, 'remove', lambda: None)
    return db.session

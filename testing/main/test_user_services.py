import pytest
from app.main.models import User
from app.main.services import user_services as us
from ..fixtures import app, db


def test_add_user_new(db, monkeypatch):
    first_name = 'Austin'
    last_name = 'Craft'
    email = 'austin@craft.com'
    age_group_1 = True
    age_group_2 = False
    age_group_3 = True

    us.add_user(
        first_name,
        last_name,
        email,
        age_group_1,
        age_group_2,
        age_group_3
    )

    u = User.query.filter_by(email=email).first()
    assert u is not None


def test_add_user_duplicate(db):
    u = User(
        first='Austin',
        last='Craft',
        email='austin@craft.com',
        age_group_1=True,
        age_group_2=False,
        age_group_3=True
    )
    db.session.add(u)
    db.session.commit()

    with pytest.raises(us.DuplicateUserError):
        us.add_user(
            u.first,
            u.last,
            u.email,
            u.age_group_1,
            u.age_group_2,
            u.age_group_3
        )

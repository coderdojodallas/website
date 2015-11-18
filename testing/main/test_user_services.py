import pytest
from app.main.models import User
from app.main.services import user_services as us


def test_add_new_user():
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


def test_add_duplicate_user(db_session):
    user = _create_user_data(db_session)

    with pytest.raises(us.DuplicateUserError):
        us.add_user(
            user.first,
            user.last,
            user.email,
            user.age_group_1,
            user.age_group_2,
            user.age_group_3
        )


def test_confirm_unconfirmed_user(db_session):
    user = _create_user_data(db_session, confirmed=False)
    user = us.confirm_user(user.email)
    assert user.confirmed


def test_confirm_invalid_user(db_session):
    with pytest.raises(us.InvalidUserError):
        us.confirm_user('austin@craft.com')


def test_confirm_already_confirmed_user(db_session):
    user = _create_user_data(db_session, confirmed=True)
    with pytest.raises(us.AlreadyConfirmedUserError):
        user = us.confirm_user(user.email)


def test_edit_user_except_email(db_session):
    user = _create_user_data(db_session, confirmed=True)
    db_session.add(user)
    db_session.commit()

    first_name = 'New'
    last_name = 'Name'
    age_group_1 = False
    age_group_2 = True
    age_group_3 = False

    user = us.edit_user(
        current_email=user.email,
        first_name=first_name,
        last_name=last_name,
        email=user.email,
        age_group_1=age_group_1,
        age_group_2=age_group_2,
        age_group_3=age_group_3
    )

    assert user.first_name == first_name
    assert user.last_name == last_name
    assert user.email == user.email
    assert user.age_group_1 == age_group_1
    assert user.age_group_2 == age_group_2
    assert user.age_group_3 == age_group_3
    assert user.confirmed


def test_edit_user_including_email(db_session):
    user = _create_user_data(db_session, confirmed=True)

    first_name = 'New'
    last_name = 'Name'
    email = 'new@name.com'
    age_group_1 = False
    age_group_2 = True
    age_group_3 = False

    user = us.edit_user(
        current_email=user.email,
        first_name=first_name,
        last_name=last_name,
        email=email,
        age_group_1=age_group_1,
        age_group_2=age_group_2,
        age_group_3=age_group_3
    )

    assert user.first_name == first_name
    assert user.last_name == last_name
    assert user.email == email
    assert user.age_group_1 == age_group_1
    assert user.age_group_2 == age_group_2
    assert user.age_group_3 == age_group_3
    assert not user.confirmed


def test_edit_invalid_user():
    first_name = 'New'
    last_name = 'Name'
    email = 'new@name.com'
    age_group_1 = False
    age_group_2 = True
    age_group_3 = False

    with pytest.raises(us.InvalidUserError):
        user = us.edit_user(
            current_email='invalid@user.com',
            first_name=first_name,
            last_name=last_name,
            email=email,
            age_group_1=age_group_1,
            age_group_2=age_group_2,
            age_group_3=age_group_3
        )


def test_edit_unconfirmed_user(db_session):
    user = _create_user_data(db_session, confirmed=False)

    first_name = 'New'
    last_name = 'Name'
    email = 'new@name.com'
    age_group_1 = False
    age_group_2 = True
    age_group_3 = False

    with pytest.raises(us.NotConfirmedUserError):
        user = us.edit_user(
            current_email=user.email,
            first_name=first_name,
            last_name=last_name,
            email=email,
            age_group_1=age_group_1,
            age_group_2=age_group_2,
            age_group_3=age_group_3
        )


def test_delete_user(db_session):
    user = _create_user_data(db_session)
    us.delete_user(user.email)
    user = User.query.filter_by(email=user.email).first()
    assert user is None


def test_delete_invalid_user():
    with pytest.raises(us.InvalidUserError):
        us.delete_user('invalid@user.com')


def test_get_user(db_session):
    user1 = _create_user_data(db_session)
    user2 = us.get_user(user1.email)
    assert user1 == user2


def test_get_invalid_user():
    with pytest.raises(us.InvalidUserError):
        us.get_user('invalid@user.com')


def _create_user_data(db_session, confirmed=False):
    user = User(
        first='Austin',
        last='Craft',
        email='austin@craft.com',
        age_group_1=True,
        age_group_2=False,
        age_group_3=True,
        confirmed=confirmed
    )
    db_session.add(user)
    db_session.commit()
    return user

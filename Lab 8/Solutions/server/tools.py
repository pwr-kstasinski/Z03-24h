from fake_database import users


def valid_user(login, password):
    return {'login': login, 'password': password} in users


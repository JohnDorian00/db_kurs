import hashlib
import uuid


def hash_password(password):
    salt = uuid.uuid4().hex
    return hashlib.sha512(salt.encode() + password.encode()).hexdigest() + ':' + salt


class User(object):
    def __init__(self, id=None, login=None, password=None, user_type=None):
        self.id = id
        self.login = login
        self.pass_hash = password
        self.user_type = user_type

    def show(self):
        print(self.id, self.login, self.pass_hash, self.user_type)

    def auth(self, verified_password):
        password, salt = self.pass_hash.split(':')
        return password == hashlib.sha512(salt.encode() + verified_password.encode()).hexdigest()

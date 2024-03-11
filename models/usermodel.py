from flask_login import UserMixin

class UserLogin(UserMixin):
    def __init__(self, user):
        self.id = user.Id
        self.username = user.username
        self.password_hash = user.password_hash

    def get_id(self):
        try:
            return str(self.id)
        except AttributeError:
            raise NotImplementedError('No `id` attribute - override `get_id`')

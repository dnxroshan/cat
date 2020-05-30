

class User:
    def __init__(self, username):
        self.username = username

    def get_id(self):
        return self.username

    def is_active(self):
        return True
    
    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True
class UserNotExistException(Exception):
    def __init__(self, message):
        super(Exception, self).__init__()
        self.message = message

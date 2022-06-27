class DisciplineIDException(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = "Invalid discipline ID!"

    def __str__(self):
        return self.message


class DisciplineNameException(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = "Invalid discipline name!"

    def __str__(self):
        return self.message

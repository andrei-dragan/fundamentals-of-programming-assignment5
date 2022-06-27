class StudentIDException(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = "Invalid student ID!"

    def __str__(self):
        return self.message


class StudentNameException(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = "Invalid student name!"

    def __str__(self):
        return self.message

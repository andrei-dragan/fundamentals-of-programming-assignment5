class Student:
    def __init__(self, student_id, name):
        self.__student_id = student_id
        self.__name = name

    @property
    def id(self):
        return self.__student_id

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, new_name):
        self.__name = new_name

    def __str__(self):
        return "student " + str(self.id) + ": " + str(self.name)

class Grade:
    def __init__(self, discipline_id, student_id, grade_value):
        self.__discipline_id = discipline_id
        self.__student_id = student_id
        self.__grade_value = grade_value

    @property
    def discipline_id(self):
        return self.__discipline_id

    @property
    def student_id(self):
        return self.__student_id

    @property
    def grade_value(self):
        return self.__grade_value

    
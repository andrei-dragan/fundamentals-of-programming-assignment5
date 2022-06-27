import random

from src.services.undo_service import FunctionCall, CascadedOperation, Operation


class GradeService:
    def __init__(self, grade_repo, student_repo, discipline_repo, undo_service):
        self.__grade_repo = grade_repo
        self.__student_repo = student_repo
        self.__discipline_repo = discipline_repo
        self.__undo_service = undo_service

    @property
    def grade_repo(self):
        return self.__grade_repo

    def __len__(self):
        return len(self.grade_repo)

    def generate_grades(self, n):
        self.__undo_service.set_record_flag(False)

        for i in range(n):
            grade_value = round(random.uniform(0.0, 10.0), 2)
            student_id = 0
            while self.__student_repo.check_id(student_id) is False:
                student_id = random.randint(1, 50)
            discipline_id = 0
            while self.__discipline_repo.check_id(discipline_id) is False:
                discipline_id = random.randint(1, 50)

            self.grade_repo.add(discipline_id, student_id, grade_value)

        self.__undo_service.set_record_flag(True)

    def add(self, discipline_id, student_id, grade_value):
        """
        Add the new grade after converting the grade_value into a float number
        :param discipline_id: The id of the discipline the grade was obtained at
        :param student_id: The id of the student who obtained the grade
        :param grade_value: The value of the grade (float)
        :return: None
        """
        try:
            grade_value = float(grade_value)
        except ValueError:
            raise GradeException("Grade must be a real number between 0 and 10!")

        if grade_value < 0 or grade_value > 10:
            raise GradeException("Grade must be a real number between 0 and 10!")

        self.grade_repo.add(discipline_id, student_id, grade_value)

        # Undo / Redo functionality
        fc_undo = FunctionCall(self.grade_repo.remove, discipline_id, student_id, grade_value)
        fc_redo = FunctionCall(self.add, discipline_id, student_id, grade_value)

        cope = CascadedOperation()
        cope.add(Operation(fc_undo, fc_redo))

        self.__undo_service.record_operation(cope)

    def list(self):
        """
        Return a list to list the grades
        :return: A list of tuples (<grade_value>, <student_id>, <discipline_id>)
        """
        return self.grade_repo.list()


class GradeException(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = "Invalid grade value!"

    def __str__(self):
        return self.message

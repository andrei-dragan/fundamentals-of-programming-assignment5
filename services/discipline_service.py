import random

from src.exceptions.discipline_exceptions import DisciplineIDException
from src.services.undo_service import FunctionCall, Operation, CascadedOperation


class DisciplineService:
    def __init__(self, discipline_repo, grade_repo, undo_service):
        self.__discipline_repo = discipline_repo
        self.__grade_repo = grade_repo
        self.__undo_service = undo_service

    @property
    def discipline_repo(self):
        return self.__discipline_repo

    @property
    def grade_repo(self):
        return self.__grade_repo

    def generate_disciplines(self, n):
        """
        Generate n randomized disciplines that are added to the list of disciplines
        :param n: The number of disciplines to be generated
        :return: None
        """
        self.__undo_service.set_record_flag(False)
        for i in range(n):
            ok = True
            discipline_id = 0
            while ok:
                discipline_id = random.randint(1, 50)
                if self.check_id(discipline_id) is False:
                    ok = False

            names = ['Math', 'Fundamentals of programming', 'Computer Science Architecture', 'HTML5', 'Python3',
                     'Biology', 'Geography', 'Physical Education', 'Physics', 'Romanian', 'English', 'German',
                     'Painting', 'Music', 'CSS3', 'JavaScript', 'Django', 'Laravel', 'React', 'Vue JS', 'C++',
                     'Algebra', 'Analysis', 'Geometry', 'Competitive Programming', 'Website Development', 'AI',
                     'History', 'Organic Chemistry']
            name_id = random.randint(0, len(names)-1)
            while self.discipline_repo.check_name(names[name_id]):
                name_id = random.randint(0, len(names) - 1)
            name = names[name_id]

            self.add(discipline_id, name)
        self.__undo_service.set_record_flag(True)

    def add(self, discipline_id, discipline_name):
        """
        Add the discipline to the list of disciplines after converting the discipline_id to an integer
        :param discipline_id: The unique id of the discipline
        :param discipline_name: The name of the discipline
        :return: None
        """
        try:
            discipline_id = int(discipline_id)
        except ValueError:
            raise DisciplineIDException("The id of the discipline is invalid!")

        if discipline_id <= 0:
            raise DisciplineIDException("The id of the discipline is invalid!")

        self.discipline_repo.add(discipline_id, discipline_name)

        # Undo / Redo functionality
        fc_undo = FunctionCall(self.remove, discipline_id)
        fc_redo = FunctionCall(self.add, discipline_id, discipline_name)

        cope = CascadedOperation()
        cope.add(Operation(fc_undo, fc_redo))

        self.__undo_service.record_operation(cope)

    def remove(self, discipline_id):
        """
        Remove the discipline from the list of disciplines and the list of grades
        after converting the discipline_id to an integer and checking if the id is valid
        :param discipline_id: The unique id of the discipline
        :return: None
        """
        try:
            discipline_id = int(discipline_id)
        except ValueError:
            raise DisciplineIDException("The id of the discipline is invalid!")

        if discipline_id <= 0:
            raise DisciplineIDException("The id of the discipline is invalid!")

        del_discipline = self.discipline_repo.remove(discipline_id)
        del_grades = self.grade_repo.discipline_remove(discipline_id)

        # Undo / Redo functionality
        fc_undo = FunctionCall(self.add, del_discipline.id, del_discipline.name)
        fc_redo = FunctionCall(self.remove, del_discipline.id)

        cope = CascadedOperation()
        cope.add(Operation(fc_undo, fc_redo))

        for grade in del_grades:
            fc_undo = FunctionCall(self.grade_repo.add, grade.discipline_id, grade.student_id, grade.grade_value)
            fc_redo = FunctionCall(self.grade_repo.remove, grade.discipline_id, grade.student_id, grade.grade_value)
            cope.add(Operation(fc_undo, fc_redo))

        self.__undo_service.record_operation(cope)

    def update(self, discipline_id, discipline_name):
        """
        Update the name of the discipline after converting the discipline_id to an integer
        :param discipline_id: The id of the discipline
        :param discipline_name: The updated name of the discipline
        :return: None
        """
        try:
            discipline_id = int(discipline_id)
        except ValueError:
            raise DisciplineIDException("The id of the discipline is invalid!")

        if discipline_id <= 0:
            raise DisciplineIDException("The id of the discipline is invalid!")

        old_name = self.discipline_repo[discipline_id]
        new_name = discipline_name
        self.discipline_repo.update(discipline_id, discipline_name)

        # Undo / Redo functionality
        fc_undo = FunctionCall(self.update, discipline_id, old_name)
        fc_redo = FunctionCall(self.update, discipline_id, new_name)

        cope = CascadedOperation()
        cope.add(Operation(fc_undo, fc_redo))

        self.__undo_service.record_operation(cope)

    def list(self):
        """
        Return a list of tuples representing the id and name of each discipline
        :return: A list of tuples (discipline_id, discipline_name)
        """
        return self.discipline_repo.list()

    def search(self, search_input):
        """
        Filter the disciplines such that the user's input is (partially) matching the id / name
        :param search_input: The user's input
        :return: A list of matching disciplines
        """
        search_input = search_input.lower()
        filtered_disciplines = self.__discipline_repo.search(search_input)
        return filtered_disciplines

    def __len__(self):
        return len(self.discipline_repo)

    def __getitem__(self, discipline_id):
        try:
            discipline_id = int(discipline_id)
        except ValueError:
            raise DisciplineIDException("The id of the discipline is invalid!")

        if discipline_id <= 0:
            raise DisciplineIDException("The id of the discipline is invalid!")

        if self.check_id(discipline_id) is not True:
            raise DisciplineIDException("This id does not exist!")

        return self.discipline_repo[discipline_id]

    def check_id(self, discipline_id):
        """
        Check if there is a discipline with the id of discipline_id after converting the discipline_id to an integer
        :param discipline_id: The id of the discipline
        :return: True if there is a discipline with the id of discipline_id, False otherwise
        """
        try:
            discipline_id = int(discipline_id)
        except ValueError:
            raise DisciplineIDException("The id of the discipline is invalid!")

        if discipline_id <= 0:
            raise DisciplineIDException("The id of the discipline is invalid!")
        return self.discipline_repo.check_id(discipline_id)

    def top(self):
        """
        :return: A sorted list of tuples consisting of the id of the discipline and its average grade
        """
        disciplines_and_grades = list()
        disciplines_ids = self.discipline_repo.get_ids()
        for discipline_id in disciplines_ids:
            grade = self.grade_repo.average_discipline(discipline_id)
            if grade != 0:
                disciplines_and_grades.append((discipline_id, grade))

        ok = True
        disciplines_and_grades_length = len(disciplines_and_grades)
        while ok:
            ok = False
            for i in range(disciplines_and_grades_length-1):
                if disciplines_and_grades[i][1] < disciplines_and_grades[i+1][1]:
                    ok = True
                    disciplines_and_grades[i], disciplines_and_grades[i+1] = \
                        disciplines_and_grades[i+1], disciplines_and_grades[i]

        return disciplines_and_grades

import random

from src.exceptions.student_exceptions import StudentIDException, StudentNameException
from src.services.undo_service import FunctionCall, CascadedOperation, Operation


class StudentService:
    def __init__(self, student_repo, grade_repo, undo_service):
        self.__student_repo = student_repo
        self.__grade_repo = grade_repo
        self.__undo_service = undo_service

    @property
    def student_repo(self):
        return self.__student_repo

    @property
    def grade_repo(self):
        return self.__grade_repo

    def generate_students(self, n):
        """
        Generate n randomized students that are added to the list of students
        :param n: The number of students to be generated
        :return: None
        """
        self.__undo_service.set_record_flag(False)
        for i in range(n):
            ok = True
            student_id = 0
            while ok:
                student_id = random.randint(1, 50)
                if self.check_id(student_id) is False:
                    ok = False

            names = ['Andrei', 'Mihai', 'George', 'Gheorghe', 'Ioana', 'Maria', 'Irina', 'Catalina', 'Catalin',
                     'Costel', 'Ciprian', 'Viorel', 'Robert', 'Alin', 'Anton', 'Augustin', 'Teodor', 'Teodora',
                     'Andreea', 'Alexandru', 'Georgiana', 'Gabriel', 'Gabriela', 'Mark', 'David', 'Rares', 'Ioan',
                     'Mara', 'Camil', 'Claudiu', 'Cornel', 'Dragos', 'Dumitru', 'Radu', 'Emilian', 'Felix', 'Horia',
                     'Diana', 'Mihaela', 'Mihael', 'Adrian', 'Adriana', 'Petru', 'Pavel', 'Sarah', 'Stefan', 'Bogdan']
            name_id = random.randint(0, len(names) - 1)
            name = names[name_id]

            self.add(student_id, name)
        self.__undo_service.set_record_flag(True)

    def add(self, student_id, student_name):
        """
        Add the student to the list of students
        after converting the student_id to an integer and validating the name
        :param student_id: The unique id of the student
        :param student_name: The name of the student
        :return: None
        """
        try:
            student_id = int(student_id)
        except ValueError:
            raise StudentIDException("The id of the student should be an integer greater than 0!")

        if student_id <= 0:
            raise StudentIDException("The id of the student should be greater than 0!")

        if not all(x.isalpha() or x.isspace() or x == '-' for x in student_name):
            raise StudentNameException("This is not a valid name!")

        self.student_repo.add(student_id, student_name)

        # Undo / Redo functionality
        fc_undo = FunctionCall(self.remove, student_id)
        fc_redo = FunctionCall(self.add, student_id, student_name)

        cope = CascadedOperation()
        cope.add(Operation(fc_undo, fc_redo))

        self.__undo_service.record_operation(cope)

    def remove(self, student_id):
        """
        Remove the student from the list of students and the list of grades
        after converting the student_id to an integer and checking if the id is valid
        :param student_id: The unique id of the student
        :return: None
        """
        try:
            student_id = int(student_id)
        except ValueError:
            raise StudentIDException("The id of the student should be an integer greater than 0!")

        if student_id <= 0:
            raise StudentIDException("The id of the student should be greater than 0!")

        del_student = self.student_repo.remove(student_id)
        del_grades = self.grade_repo.student_remove(student_id)

        # Undo / Redo functionality
        fc_undo = FunctionCall(self.add, del_student.id, del_student.name)
        fc_redo = FunctionCall(self.remove, del_student.id)

        cope = CascadedOperation()
        cope.add(Operation(fc_undo, fc_redo))

        for grade in del_grades:
            fc_undo = FunctionCall(self.grade_repo.add, grade.discipline_id, grade.student_id, grade.grade_value)
            fc_redo = FunctionCall(self.grade_repo.remove, grade.discipline_id, grade.student_id, grade.grade_value)
            cope.add(Operation(fc_undo, fc_redo))

        self.__undo_service.record_operation(cope)

    def update(self, student_id, student_name):
        """
        Update the name of the student after converting the student_id to an integer and validating the name
        :param student_id: The id of the student
        :param student_name: The updated name of the student
        :return: None
        """
        try:
            student_id = int(student_id)
        except ValueError:
            raise StudentIDException("The id of the student should be an integer greater than 0!")

        if student_id <= 0:
            raise StudentIDException("The id of the student should be greater than 0!")

        if not all(x.isalpha() or x.isspace() or x == '-' for x in student_name):
            raise StudentNameException("This is not a valid name!")

        old_name = self.student_repo[student_id]
        new_name = student_name
        self.student_repo.update(student_id, student_name)

        # Undo / Redo functionality
        fc_undo = FunctionCall(self.update, student_id, old_name)
        fc_redo = FunctionCall(self.update, student_id, new_name)

        cope = CascadedOperation()
        cope.add(Operation(fc_undo, fc_redo))

        self.__undo_service.record_operation(cope)

    def list(self):
        """
        Return a list of tuples representing the id and name of each student
        :return: A list of tuples (student_id, student_name)
        """
        return self.student_repo.list()

    def search(self, search_input):
        """
        Filter the students such that the user's input is (partially) matching the id / name
        :param search_input: The user's input
        :return: A list of matching students
        """
        search_input = search_input.lower()
        filtered_students = self.__student_repo.search(search_input)
        return filtered_students

    def failed(self):
        """
        Find students failing at one or more disciplines
        :return: A dictionary of student's ids together with the ids of the failed disciplines
        """
        failed_students = dict()
        students_ids = self.student_repo.get_ids()
        for student_id in students_ids:
            failed_disciplines = self.grade_repo.failed(student_id)
            if len(failed_disciplines) != 0:
                failed_students[student_id] = failed_disciplines
        return failed_students

    def top(self):
        """
        :return: A sorted list of tuples consisting of the id of the student and its average grade
        """
        students_and_grades = list()
        students_ids = self.student_repo.get_ids()
        for student_id in students_ids:
            students_and_grades.append((student_id, self.grade_repo.average_student(student_id)))

        ok = True
        students_and_grades_length = len(students_and_grades)
        while ok:
            ok = False
            for i in range(students_and_grades_length-1):
                if students_and_grades[i][1] < students_and_grades[i+1][1]:
                    ok = True
                    students_and_grades[i], students_and_grades[i+1] = students_and_grades[i+1], students_and_grades[i]

        return students_and_grades


    def __len__(self):
        return len(self.student_repo)

    def __getitem__(self, student_id):
        """
        Return the name of the student having the id of student_id, after validating the id
        :param student_id: The id of the student
        :return: A string representing the name of the student having the id of student_id
        """
        try:
            student_id = int(student_id)
        except ValueError:
            raise StudentIDException("The id of the student should be an integer greater than 0!")

        if student_id <= 0:
            raise StudentIDException("The id of the student should be greater than 0!")

        if self.check_id(student_id) is False:
            raise StudentIDException("This id does not exist!")

        return self.student_repo[student_id]

    def check_id(self, student_id):
        """
        Check if there is a student with the id of student_id after converting the student_id to an integer
        :param student_id: The id of the student
        :return: True if there is a student with the id of student_id, False otherwise
        """
        try:
            student_id = int(student_id)
        except ValueError:
            raise StudentIDException("The id of the student should be an integer greater than 0!")

        if student_id <= 0:
            raise StudentIDException("The id of the student should be greater than 0!")

        return self.student_repo.check_id(student_id)

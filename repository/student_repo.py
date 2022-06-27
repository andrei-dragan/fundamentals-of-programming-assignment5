from src.domain.student.student import Student
from src.exceptions.student_exceptions import StudentIDException


class StudentRepository:
    def __init__(self):
        self.__students = list()

    @property
    def students(self):
        return self.__students

    @students.setter
    def students(self, students):
        self.__students = students

    def check_id(self, student_id):
        """
        Check if there is a student with the id of student_id
        :param student_id: The id of the student
        :return: True if there is a student with the id of student_id, False otherwise
        """
        for student in self.students:
            if student.id == student_id:
                return True
        return False

    def add(self, student_id, student_name):
        """
        Add a student to the list of students after validating the uniqueness of the id and creating the object
        student, based on the id and name
        :param student_id: The id of the student we want to add
        :param student_name: The name of the student we want to add
        :return: None
        """
        if self.check_id(student_id):
            raise StudentIDException("A student with this ID already exists!")

        student = Student(student_id, student_name)
        self.students.append(student)

    def remove(self, student_id):
        """
        Remove the student from the list of students, if it exists
        :param student_id: The id of the student we want to remove
        :return: The student object that was deleted
        """
        if not self.check_id(student_id):
            raise StudentIDException("A student with this ID does not exist!")

        for student in self.students:
            if student.id == student_id:
                self.students.remove(student)
                return student

    def update(self, student_id, student_name):
        """
        Update the name of a student, if the student exists in the list of students
        :param student_id: The unique id of the student
        :param student_name: The updated name of the student
        :return: None
        """
        if not self.check_id(student_id):
            raise StudentIDException("A student with this ID does not exist!")

        for student in self.students:
            if student.id == student_id:
                student.name = student_name

    def __len__(self):
        return len(self.students)

    def __getitem__(self, student_id):
        if self.check_id(student_id) is False:
            raise StudentIDException("A student with this ID does not exist!")

        for student in self.students:
            if student.id == student_id:
                return student.name

    def list(self):
        """
        Return a list of tuples representing the id and name of each student
        :return: A list of tuples (student_id, student_name)
        """
        answer = list()
        for student in self.students:
            answer.append((student.id, student.name))
        return answer

    def search(self, search_input):
        """
        Filter the students such that the user's input is (partially) matching the id / name
        :param search_input: The user's input
        :return: A list of matching students
        """
        filtered_students = list()
        for student in self.students:
            student_id = str(student.id).lower()
            student_name = str(student.name).lower()
            if search_input in student_id or search_input in student_name:
                filtered_students.append(student)
        return filtered_students

    def get_ids(self):
        ids = list()
        for student in self.students:
            ids.append(student.id)
        return ids

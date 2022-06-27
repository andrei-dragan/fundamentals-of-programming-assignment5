import unittest

from src.domain.discipline.discipline import Discipline
from src.domain.student.student import Student


class DisciplineDomainTest(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_str_discipline(self):
        discipline = Discipline(2, 'Math')
        self.assertEqual(str(discipline), 'discipline 2: Math')

    def tearDown(self) -> None:
        pass


class StudentDomainTest(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_str_student(self):
        student = Student(2, 'Mihai')
        self.assertEqual(str(student), 'student 2: Mihai')

    def tearDown(self) -> None:
        pass

import unittest

from src.repository.grade_repo import GradeRepository


class StudentRepositoryTest(unittest.TestCase):
    def setUp(self):
        """
        Runs before any of the tests
        Used to set up the class so that tests can be run
        :return: None
        """
        self.__repo = GradeRepository()
        self.__repo.add(1, 1, 10)
        self.__repo.add(2, 1, 8.5)

    def test_add(self):
        self.assertEqual(len(self.__repo), 2)
        self.__repo.add(3, 1, 5)
        self.assertEqual(len(self.__repo), 3)

    def test_list(self):
        self.assertEqual(self.__repo.list(), [(10, 1, 1), (8.5, 1, 2)])

    def test_discipline_remove(self):
        self.__repo.discipline_remove(2)
        self.assertEqual(len(self.__repo), 1)

    def test_student_remove(self):
        self.__repo.student_remove(1)
        self.assertEqual(len(self.__repo), 0)

    def test_failed(self):
        self.__repo.add(3, 2, 2)
        self.__repo.add(3, 2, 6)
        self.__repo.add(5, 2, 2)
        self.assertEqual(self.__repo.failed(2), [3, 5])
        self.assertEqual(self.__repo.failed(1), [])

    def test_average_student(self):
        self.__repo.add(3, 2, 2)
        self.__repo.add(3, 2, 6)
        self.__repo.add(5, 2, 2)
        self.assertEqual(self.__repo.average_student(1), 9.25)
        self.assertEqual(self.__repo.average_student(2), 3)
        self.assertEqual(self.__repo.average_student(3), 0)

    def test_average_discipline(self):
        self.__repo.add(1, 2, 2)
        self.__repo.add(2, 2, 6)
        self.__repo.add(2, 2, 2)
        self.assertEqual(self.__repo.average_discipline(1), 6)
        self.assertEqual(self.__repo.average_discipline(2), 5.5)
        self.assertEqual(self.__repo.average_discipline(3), 0)

    def tearDown(self) -> None:
        """
        Runs after every test method
        """
        pass

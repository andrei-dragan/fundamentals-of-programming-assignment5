import unittest

from src.repository.discipline_repo import DisciplineRepository
from src.repository.grade_repo import GradeRepository
from src.repository.student_repo import StudentRepository
from src.services.grade_service import GradeService, GradeException
from src.services.undo_service import UndoService


class GradeServiceTest(unittest.TestCase):
    def setUp(self) -> None:
        self.__student_repo = StudentRepository()
        self.__discipline_repo = DisciplineRepository()
        self.__grade_repo = GradeRepository()
        self.__undo_service = UndoService()

        self.__service = GradeService(self.__grade_repo, self.__student_repo, self.__discipline_repo,
                                      self.__undo_service)

        self.__service.add(2, 2, 3)
        self.__service.add(2, 5, 5.6)

    def test_service_add(self):
        self.__service.add(3, 2, 3)
        self.__service.add(3, 5, 5.6)
        self.assertEqual(len(self.__service), 4)

        with self.assertRaises(GradeException):
            self.__service.add(1, 2, -1)
        with self.assertRaises(GradeException):
            self.__service.add(1, 2, 11)
        with self.assertRaises(GradeException):
            self.__service.add(1, 2, 'abc')

    def test_service_list(self):
        self.assertEqual(self.__service.list(), [(3, 2, 2), (5.6, 5, 2)])

    def test_generate_grades(self):
        self.__discipline_repo.add(1, 'Math')
        self.__discipline_repo.add(2, 'Biology')
        self.__student_repo.add(1, 'Mihai')
        self.__student_repo.add(2, 'Andrei')

        self.__service.generate_grades(5)
        self.assertEqual(len(self.__service), 7)

    def tearDown(self) -> None:
        pass

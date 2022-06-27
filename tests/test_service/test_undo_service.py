import unittest

from src.repository.discipline_repo import DisciplineRepository
from src.repository.grade_repo import GradeRepository
from src.repository.student_repo import StudentRepository
from src.services.discipline_service import DisciplineService
from src.services.student_service import StudentService
from src.services.undo_service import UndoService, UndoException


class UndoServiceTest(unittest.TestCase):
    def setUp(self) -> None:
        self.__student_repo = StudentRepository()
        self.__grade_repo = GradeRepository()
        self.__discipline_repo = DisciplineRepository()
        self.__undo_service = UndoService()
        self.__student_service = StudentService(self.__student_repo, self.__grade_repo, self.__undo_service)
        self.__discipline_service = DisciplineService(self.__discipline_repo, self.__grade_repo, self.__undo_service)

    def test_undo_redo_student(self):
        self.__student_service.add(23, 'Mihai')
        self.__student_service.add(50, 'George')
        self.__undo_service.undo()
        self.assertEqual(len(self.__student_service), 1)
        self.__undo_service.undo()
        self.assertEqual(len(self.__student_service), 0)

        with self.assertRaises(UndoException):
            self.__undo_service.undo()

        self.__undo_service.redo()
        self.__undo_service.redo()
        self.assertEqual(len(self.__student_service), 2)

        with self.assertRaises(UndoException):
            self.__undo_service.redo()

    def test_undo_redo_discipline(self):
        self.__discipline_service.add(23, 'Math')
        self.__discipline_service.add(50, 'Biology')
        self.__undo_service.undo()
        self.assertEqual(len(self.__discipline_service), 1)
        self.__undo_service.undo()
        self.assertEqual(len(self.__discipline_service), 0)

        with self.assertRaises(UndoException):
            self.__undo_service.undo()

        self.__undo_service.redo()
        self.__undo_service.redo()
        self.assertEqual(len(self.__discipline_service), 2)

        with self.assertRaises(UndoException):
            self.__undo_service.redo()

    def tearDown(self) -> None:
        pass

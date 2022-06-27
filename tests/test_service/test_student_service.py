import unittest

from src.repository.grade_repo import GradeRepository
from src.repository.student_repo import StudentRepository, StudentIDException, StudentNameException
from src.services.student_service import StudentService
from src.services.undo_service import UndoService


class StudentServiceTest(unittest.TestCase):
    def setUp(self):
        """
        Runs before any of the tests
        Used to set up the class so that tests can be run
        :return: None
        """
        self.__student_repo = StudentRepository()
        self.__grade_repo = GradeRepository()
        self.__undo_service = UndoService()
        self.__service = StudentService(self.__student_repo, self.__grade_repo, self.__undo_service)

        self.__service.add(10, 'Andrei')
        self.__service.add(11, 'George')

    def test_service_add(self):
        self.assertEqual(len(self.__service), 2)
        self.__service.add(13, 'Gheorghe')
        self.assertEqual(len(self.__service), 3)
        self.assertEqual(self.__service[10], 'Andrei')
        self.assertEqual(self.__service[11], 'George')
        self.assertEqual(self.__service[13], 'Gheorghe')

    def test_service_add_exception(self):
        with self.assertRaises(StudentIDException):
            self.__service.add(-2, 'Mihai')
        with self.assertRaises(StudentIDException):
            self.__service.add('random', 'Mihai')

        with self.assertRaises(StudentNameException):
            self.__service.add(20, 'Mihai23')
        with self.assertRaises(StudentNameException):
            self.__service.add(20, '1034')
        with self.assertRaises(StudentNameException):
            self.__service.add(20, '@_')

    def test_service_remove(self):
        self.__service.remove(10)
        self.assertEqual(len(self.__service), 1)
        self.assertEqual(self.__service[11], 'George')

        with self.assertRaises(StudentIDException):
            x = self.__service[10]

    def test_service_remove_exception(self):
        with self.assertRaises(StudentIDException):
            self.__service.remove(-2)
        with self.assertRaises(StudentIDException):
            self.__service.remove('random')

    def test_service_update(self):
        self.__service.update(10, 'Mihai')
        self.assertEqual(self.__service[10], 'Mihai')
        self.__service.update(10, 'George')
        self.assertEqual(self.__service[10], 'George')

    def test_service_update_exception(self):
        with self.assertRaises(StudentIDException):
            self.__service.update(-2, 'Mihai')
        with self.assertRaises(StudentIDException):
            self.__service.update('random', 'Mihai')

        with self.assertRaises(StudentNameException):
            self.__service.update(10, 'Mihai23')
        with self.assertRaises(StudentNameException):
            self.__service.update(10, '1034')
        with self.assertRaises(StudentNameException):
            self.__service.update(10, '@_')

    def test_service_list(self):
        self.assertEqual(self.__service.list(), [(10, 'Andrei'), (11, 'George')])

    def test_generate_students(self):
        self.__service.generate_students(10)
        self.assertEqual(len(self.__service), 12)

    def test_search(self):
        self.assertEqual(self.__service.search('11'), [self.__service.student_repo.students[1]])
        self.assertEqual(self.__service.search('10'), [self.__service.student_repo.students[0]])
        self.assertEqual(self.__service.search('anDrEi'), [self.__service.student_repo.students[0]])
        self.assertEqual(self.__service.search('ORG'), [self.__service.student_repo.students[1]])
        self.assertEqual(self.__service.search('1'), [self.__service.student_repo.students[0],
                                                      self.__service.student_repo.students[1]])
        self.assertEqual(self.__service.search('r'), [self.__service.student_repo.students[0],
                                                      self.__service.student_repo.students[1]])

    def test_failed(self):
        self.__service.add(2, 'Mihai')
        self.__service.add(1, 'Marian')
        self.__service.add(5, 'Viorel')
        self.__service.grade_repo.add(1, 1, 10)
        self.__service.grade_repo.add(2, 1, 8.5)
        self.__service.grade_repo.add(3, 2, 2)
        self.__service.grade_repo.add(3, 2, 6)
        self.__service.grade_repo.add(7, 2, 1)
        self.__service.grade_repo.add(4, 5, 2)
        self.assertEqual(self.__service.failed(), {2: [3, 7], 5: [4]})

    def test_top(self):
        self.__service.add(2, 'Mihai')
        self.__service.add(1, 'Marian')
        self.__service.add(5, 'Viorel')
        self.__service.grade_repo.add(1, 1, 10)
        self.__service.grade_repo.add(2, 1, 8.5)
        self.__service.grade_repo.add(3, 2, 2)
        self.__service.grade_repo.add(3, 2, 6)
        self.__service.grade_repo.add(7, 2, 1)
        self.__service.grade_repo.add(4, 5, 2)
        self.assertEqual(self.__service.top(), [(1, 9.25), (2, 2.5), (5, 2), (10, 0), (11, 0)])

    def test_check_id(self):
        self.assertEqual(self.__service.check_id(10), True)
        self.assertEqual(self.__service.check_id(12), False)
        with self.assertRaises(StudentIDException):
            self.__service.check_id(-2)
        with self.assertRaises(StudentIDException):
            self.__service.check_id('text')

    def tearDown(self) -> None:
        """
        Runs after every test method
        """
        pass

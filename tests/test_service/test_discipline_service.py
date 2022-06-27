import unittest

from src.repository.discipline_repo import DisciplineRepository, DisciplineIDException
from src.repository.grade_repo import GradeRepository
from src.services.discipline_service import DisciplineService
from src.services.undo_service import UndoService


class DisciplineServiceTest(unittest.TestCase):
    def setUp(self):
        """
        Runs before any of the tests
        Used to set up the class so that tests can be run
        :return: None
        """
        self.__discipline_repo = DisciplineRepository()
        self.__grade_repo = GradeRepository()
        self.__undo_service = UndoService()
        self.__service = DisciplineService(self.__discipline_repo, self.__grade_repo, self.__undo_service)

        self.__service.add(10, 'Math')
        self.__service.add(11, 'Biology')

    def test_service_add(self):
        self.assertEqual(len(self.__service), 2)
        self.__service.add(13, 'Geography')
        self.assertEqual(len(self.__service), 3)
        self.assertEqual(self.__service[10], 'Math')
        self.assertEqual(self.__service[11], 'Biology')
        self.assertEqual(self.__service[13], 'Geography')

    def test_service_add_exception(self):
        with self.assertRaises(DisciplineIDException):
            self.__service.add(-2, 'Geography')
        with self.assertRaises(DisciplineIDException):
            self.__service.add('random', 'Geography')

    def test_service_remove(self):
        self.__service.remove(10)
        self.assertEqual(len(self.__service), 1)
        self.assertEqual(self.__service[11], 'Biology')

        with self.assertRaises(DisciplineIDException):
            x = self.__service[10]

    def test_service_remove_exception(self):
        with self.assertRaises(DisciplineIDException):
            self.__service.remove(-2)
        with self.assertRaises(DisciplineIDException):
            self.__service.remove('random')

    def test_service_update(self):
        self.__service.update(10, 'Geography')
        self.assertEqual(self.__service[10], 'Geography')
        self.__service.update(10, 'Algebra')
        self.assertEqual(self.__service[10], 'Algebra')

    def test_service_update_exception(self):
        with self.assertRaises(DisciplineIDException):
            self.__service.update(-2, 'Algebra')
        with self.assertRaises(DisciplineIDException):
            self.__service.update('random', 'Biology')

    def test_service_list(self):
        self.assertEqual(self.__service.list(), [(10, 'Math'), (11, 'Biology')])

    def test_generate_students(self):
        self.__service.generate_disciplines(10)
        self.assertEqual(len(self.__service), 12)

    def test_search(self):
        self.assertEqual(self.__service.search('11'), [self.__service.discipline_repo.disciplines[1]])
        self.assertEqual(self.__service.search('10'), [self.__service.discipline_repo.disciplines[0]])
        self.assertEqual(self.__service.search('MaTh'), [self.__service.discipline_repo.disciplines[0]])
        self.assertEqual(self.__service.search('olo'), [self.__service.discipline_repo.disciplines[1]])
        self.assertEqual(self.__service.search('1'), [self.__service.discipline_repo.disciplines[0],
                                                      self.__service.discipline_repo.disciplines[1]])

    def test_top(self):
        self.__service.add(2, 'Geography')
        self.__service.add(1, 'Music')
        self.__service.add(5, 'Algebra')
        self.__service.grade_repo.add(1, 1, 10)
        self.__service.grade_repo.add(1, 2, 8.5)
        self.__service.grade_repo.add(2, 3, 2)
        self.__service.grade_repo.add(2, 3, 6)
        self.__service.grade_repo.add(2, 7, 1)
        self.__service.grade_repo.add(5, 3, 2)
        self.assertEqual(self.__service.top(), [(1, 9.25), (2, 3), (5, 2)])

    def test_check_id(self):
        self.assertEqual(self.__service.check_id(10), True)
        self.assertEqual(self.__service.check_id(12), False)
        with self.assertRaises(DisciplineIDException):
            self.__service.check_id(-2)
        with self.assertRaises(DisciplineIDException):
            self.__service.check_id('text')

    def test_get_item(self):
        with self.assertRaises(DisciplineIDException):
            x = self.__service[-2]
        with self.assertRaises(DisciplineIDException):
            x = self.__service[9]
        with self.assertRaises(DisciplineIDException):
            x = self.__service['text']

    def tearDown(self) -> None:
        """
        Runs after every test method
        """
        pass

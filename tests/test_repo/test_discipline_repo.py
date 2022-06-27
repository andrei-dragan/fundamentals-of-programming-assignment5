import unittest

from src.repository.discipline_repo import DisciplineRepository, DisciplineIDException, DisciplineNameException


class DisciplineRepositoryTest(unittest.TestCase):
    def setUp(self):
        """
        Runs before any of the tests
        Used to set up the class so that tests can be run
        :return: None
        """
        self.__repo = DisciplineRepository()
        self.__repo.add(10, 'Math')
        self.__repo.add(11, 'Biology')

    def test_repo_add(self):
        self.assertEqual(len(self.__repo), 2)
        self.__repo.add(13, 'Geography')
        self.assertEqual(len(self.__repo), 3)
        self.assertEqual(self.__repo[10], 'Math')
        self.assertEqual(self.__repo[11], 'Biology')
        self.assertEqual(self.__repo[13], 'Geography')

    def test_repo_add_exception(self):
        with self.assertRaises(DisciplineIDException):
            self.__repo.add(10, 'Algebra')
        with self.assertRaises(DisciplineIDException):
            self.__repo.add(11, 'Algebra')

        with self.assertRaises(DisciplineNameException):
            self.__repo.add(12, 'Math')

    def test_repo_remove(self):
        self.__repo.remove(10)
        self.assertEqual(len(self.__repo), 1)
        self.assertEqual(self.__repo[11], 'Biology')

        with self.assertRaises(DisciplineIDException):
            x = self.__repo[10]

    def test_repo_remove_exception(self):
        with self.assertRaises(DisciplineIDException):
            self.__repo.remove(20)

    def test_repo_update(self):
        self.__repo.update(10, 'Algebra')
        self.assertEqual(self.__repo[10], 'Algebra')
        self.__repo.update(10, 'Analysis')
        self.assertEqual(self.__repo[10], 'Analysis')

    def test_repo_update_exception(self):
        with self.assertRaises(DisciplineIDException):
            self.__repo.update(20, 'Algebra')

        with self.assertRaises(DisciplineNameException):
            self.__repo.update(11, 'Math')

    def test_repo_list(self):
        self.assertEqual(self.__repo.list(), [(10, 'Math'), (11, 'Biology')])

    def test_search(self):
        self.assertEqual(self.__repo.search('11'), [self.__repo.disciplines[1]])
        self.assertEqual(self.__repo.search('10'), [self.__repo.disciplines[0]])
        self.assertEqual(self.__repo.search('math'), [self.__repo.disciplines[0]])
        self.assertEqual(self.__repo.search('olo'), [self.__repo.disciplines[1]])
        self.assertEqual(self.__repo.search('1'), [self.__repo.disciplines[0], self.__repo.disciplines[1]])

    def test_get_ids(self):
        self.assertEqual(self.__repo.get_ids(), [10, 11])

    def test_student_id_exception(self):
        exception = DisciplineIDException()
        self.assertEqual(exception.message, 'Invalid discipline ID!')

    def test_student_name_exception(self):
        exception = DisciplineNameException()
        self.assertEqual(exception.message, 'Invalid discipline name!')

    def tearDown(self) -> None:
        """
        Runs after every test method
        """
        pass

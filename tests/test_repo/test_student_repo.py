import unittest

from src.repository.student_repo import StudentRepository, StudentIDException, StudentNameException


class StudentRepositoryTest(unittest.TestCase):
    def setUp(self):
        """
        Runs before any of the tests
        Used to set up the class so that tests can be run
        :return: None
        """
        self.__repo = StudentRepository()
        self.__repo.add(10, 'Andrei')
        self.__repo.add(11, 'George')

    def test_repo_add(self):
        self.assertEqual(len(self.__repo), 2)
        self.__repo.add(13, 'Gheorghe')
        self.assertEqual(len(self.__repo), 3)
        self.assertEqual(self.__repo[10], 'Andrei')
        self.assertEqual(self.__repo[11], 'George')
        self.assertEqual(self.__repo[13], 'Gheorghe')

    def test_repo_add_exception(self):
        with self.assertRaises(StudentIDException):
            self.__repo.add(10, 'Mihai')
        with self.assertRaises(StudentIDException):
            self.__repo.add(11, 'Mihai')

    def test_repo_remove(self):
        self.__repo.remove(10)
        self.assertEqual(len(self.__repo), 1)
        self.assertEqual(self.__repo[11], 'George')

        with self.assertRaises(StudentIDException):
            x = self.__repo[10]

    def test_repo_remove_exception(self):
        with self.assertRaises(StudentIDException):
            self.__repo.remove(20)

    def test_repo_update(self):
        self.__repo.update(10, 'Mihai')
        self.assertEqual(self.__repo[10], 'Mihai')
        self.__repo.update(10, 'George')
        self.assertEqual(self.__repo[10], 'George')

    def test_repo_update_exception(self):
        with self.assertRaises(StudentIDException):
            self.__repo.update(20, 'Mihai')

    def test_repo_list(self):
        self.assertEqual(self.__repo.list(), [(10, 'Andrei'), (11, 'George')])

    def test_search(self):
        self.assertEqual(self.__repo.search('11'), [self.__repo.students[1]])
        self.assertEqual(self.__repo.search('10'), [self.__repo.students[0]])
        self.assertEqual(self.__repo.search('andrei'), [self.__repo.students[0]])
        self.assertEqual(self.__repo.search('org'), [self.__repo.students[1]])
        self.assertEqual(self.__repo.search('1'), [self.__repo.students[0], self.__repo.students[1]])
        self.assertEqual(self.__repo.search('r'), [self.__repo.students[0], self.__repo.students[1]])

    def test_get_ids(self):
        self.assertEqual(self.__repo.get_ids(), [10, 11])

    def test_student_id_exception(self):
        exception = StudentIDException()
        self.assertEqual(exception.message, 'Invalid student ID!')

    def test_student_name_exception(self):
        exception = StudentNameException()
        self.assertEqual(exception.message, 'Invalid student name!')

    def tearDown(self) -> None:
        """
        Runs after every test method
        """
        pass

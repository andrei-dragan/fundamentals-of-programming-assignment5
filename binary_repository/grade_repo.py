import pickle

from src.repository.grade_repo import GradeRepository


class GradeBinaryFileRepository(GradeRepository):
    def __init__(self):
        super().__init__()
        self.__file_name = 'binary_files/grades.bin'
        self.__load_file()

    def __load_file(self):
        f = open(self.__file_name, "rb")
        self.grades = pickle.load(f)
        f.close()

    def __save_file(self):
        f = open(self.__file_name, "wb")
        pickle.dump(self.grades, f)
        f.close()

    def add(self, discipline_id, student_id, grade_value):
        super(GradeBinaryFileRepository, self).add(discipline_id, student_id, grade_value)
        self.__save_file()

    def remove(self, discipline_id, student_id, grade_value):
        super(GradeBinaryFileRepository, self).remove(discipline_id, student_id, grade_value)
        self.__save_file()

    def discipline_remove(self, discipline_id):
        deleted_grades = super(GradeBinaryFileRepository, self).discipline_remove(discipline_id)
        self.__save_file()
        return deleted_grades

    def student_remove(self, student_id):
        deleted_grades = super(GradeBinaryFileRepository, self).student_remove(student_id)
        self.__save_file()
        return deleted_grades

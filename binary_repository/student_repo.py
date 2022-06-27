from src.repository.student_repo import StudentRepository
import pickle

class StudentBinaryFileRepository(StudentRepository):
    def __init__(self):
        super().__init__()
        self.__file_name = 'binary_files/students.bin'
        self.__load_file()

    def __load_file(self):
        f = open(self.__file_name, "rb")
        self.students = pickle.load(f)
        f.close()

    def __save_file(self):
        f = open(self.__file_name, "wb")
        pickle.dump(self.students, f)
        f.close()

    def add(self, student_id, student_name):
        super(StudentBinaryFileRepository, self).add(student_id, student_name)
        self.__save_file()

    def update(self, student_id, student_name):
        super(StudentBinaryFileRepository, self).update(student_id, student_name)
        self.__save_file()

    def remove(self, student_id):
        deleted_student = super(StudentBinaryFileRepository, self).remove(student_id)
        self.__save_file()
        return deleted_student

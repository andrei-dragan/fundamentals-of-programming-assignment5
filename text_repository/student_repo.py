from src.repository.student_repo import StudentRepository


class StudentTextFileRepository(StudentRepository):
    def __init__(self):
        super().__init__()
        self.__file_name = 'txt_files/students.txt'
        self.__load_file()

    def __load_file(self):
        f = open(self.__file_name, "rt")
        for line in f.readlines():
            student_id, student_name = line.split(maxsplit=1, sep=' ')
            self.add(int(student_id.strip()), student_name.strip())
        f.close()

    def __save_file(self):
        f = open(self.__file_name, "wt")

        for student in self.students:
            f.write(str(student.id) + ' ' + student.name + '\n')

        f.close()

    def add(self, student_id, student_name):
        super(StudentTextFileRepository, self).add(student_id, student_name)
        self.__save_file()

    def update(self, student_id, student_name):
        super(StudentTextFileRepository, self).update(student_id, student_name)
        self.__save_file()

    def remove(self, student_id):
        deleted_student = super(StudentTextFileRepository, self).remove(student_id)
        self.__save_file()
        return deleted_student

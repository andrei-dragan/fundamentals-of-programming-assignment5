from src.repository.grade_repo import GradeRepository


class GradeTextFileRepository(GradeRepository):
    def __init__(self):
        super().__init__()
        self.__file_name = 'txt_files/grades.txt'
        self.__load_file()

    def __load_file(self):
        f = open(self.__file_name, "rt")
        for line in f.readlines():
            discipline_id, student_id, grade_value = line.split(maxsplit=2, sep=' ')
            self.add(int(discipline_id.strip()), int(student_id.strip()), float(grade_value.strip()))
        f.close()

    def __save_file(self):
        f = open(self.__file_name, "wt")

        for grade in self.grades:
            f.write(str(grade.discipline_id) + ' ' + str(grade.student_id) + ' ' + str(grade.grade_value) + '\n')

        f.close()

    def add(self, discipline_id, student_id, grade_value):
        super(GradeTextFileRepository, self).add(discipline_id, student_id, grade_value)
        self.__save_file()

    def remove(self, discipline_id, student_id, grade_value):
        super(GradeTextFileRepository, self).remove(discipline_id, student_id, grade_value)
        self.__save_file()

    def discipline_remove(self, discipline_id):
        deleted_grades = super(GradeTextFileRepository, self).discipline_remove(discipline_id)
        self.__save_file()
        return deleted_grades

    def student_remove(self, student_id):
        deleted_grades = super(GradeTextFileRepository, self).student_remove(student_id)
        self.__save_file()
        return deleted_grades

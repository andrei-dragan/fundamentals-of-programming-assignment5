from src.domain.grade.grade import Grade


class GradeRepository:
    def __init__(self):
        self.__grades = list()

    @property
    def grades(self):
        return self.__grades

    @grades.setter
    def grades(self, grades):
        self.__grades = grades

    def add(self, discipline_id, student_id, grade_value):
        """
        Add the new grade value
        :param discipline_id: The id of the discipline the grade was obtained at
        :param student_id: The id of the student who obtained the grade
        :param grade_value: The value of the grade (float)
        :return: None
        """
        self.grades.append(Grade(discipline_id, student_id, grade_value))

    def remove(self, discipline_id, student_id, grade_value):
        """
        Remove one grade with this attributes
        :param discipline_id: The id of the discipline the grade was obtained at
        :param student_id: The id of the student who obtained the grade
        :param grade_value: The value of the grade (float)
        :return: None
        """
        for grade in self.grades:
            if grade.discipline_id == discipline_id and \
                    grade.student_id == student_id and \
                    grade.grade_value == grade_value:
                self.grades.remove(grade)
                return

    def list(self):
        """
        Create a list of tuples used further to display the grades
        :return: A list of tuples (<grade_value>, <student_id>, <discipline_id>)
        """
        answer = list()
        for grade in self.grades:
            answer.append((grade.grade_value, grade.student_id, grade.discipline_id))

        return answer

    def discipline_remove(self, discipline_id):
        """
        Remove all the grades assigned to the discipline having the id of discipline_id
        :param discipline_id: The id of the discipline
        :return: A list of grades that were deleted
        """
        deleted_grades = []
        ok = True
        while ok:
            ok = False
            for grade in self.grades:
                if grade.discipline_id == discipline_id:
                    deleted_grades.append(grade)
                    self.__grades.remove(grade)
                    ok = True

        return deleted_grades

    def student_remove(self, student_id):
        """
        Remove all the grades obtained by the student having the id of student_id
        :param student_id: The id of the student
        :return: A list of grades that were deleted
        """
        deleted_grades = []
        ok = True
        while ok:
            ok = False
            for grade in self.grades:
                if grade.student_id == student_id:
                    deleted_grades.append(grade)
                    self.grades.remove(grade)
                    ok = True

        return deleted_grades

    def failed(self, student_id):
        """
        Find the disciplines where the student with the student_id failed
        :param student_id: The id of the student
        :return: A list of id_disciplines, representing the disciplines the student failed at
        """
        student_disciplines = dict()
        failed_disciplines = list()
        for grade in self.grades:
            if grade.student_id == student_id:
                if grade.discipline_id in student_disciplines:
                    student_disciplines[grade.discipline_id]['nr'] += 1
                    student_disciplines[grade.discipline_id]['sum'] += grade.grade_value
                else:
                    student_disciplines[grade.discipline_id] = {}
                    student_disciplines[grade.discipline_id]['nr'] = 1
                    student_disciplines[grade.discipline_id]['sum'] = grade.grade_value

        for discipline in student_disciplines:
            average = student_disciplines[discipline]['sum'] / student_disciplines[discipline]['nr']
            if average < 5:
                failed_disciplines.append(discipline)

        return failed_disciplines

    def average_student(self, student_id):
        """
        Compute the average grade
        :param student_id: The id of the student
        :return: A float value, representing the average grade
        """
        student_disciplines = dict()
        total_average = 0
        no_disciplines = 0

        for grade in self.grades:
            if grade.student_id == student_id:
                if grade.discipline_id in student_disciplines:
                    student_disciplines[grade.discipline_id]['nr'] += 1
                    student_disciplines[grade.discipline_id]['sum'] += grade.grade_value
                else:
                    student_disciplines[grade.discipline_id] = {}
                    student_disciplines[grade.discipline_id]['nr'] = 1
                    student_disciplines[grade.discipline_id]['sum'] = grade.grade_value

        for discipline in student_disciplines:
            discipline_average = student_disciplines[discipline]['sum'] / student_disciplines[discipline]['nr']
            total_average += discipline_average
            no_disciplines += 1

        if no_disciplines != 0:
            return total_average / no_disciplines
        else:
            return 0

    def average_discipline(self, discipline_id):
        """
        Find the average grade of a discipline
        :param discipline_id: The id of the discipline
        :return: The average grade of the discipline
        """
        total_average = 0
        no_grades = 0

        for grade in self.grades:
            if grade.discipline_id == discipline_id:
                total_average += grade.grade_value
                no_grades += 1

        if no_grades != 0:
            return total_average / no_grades
        else:
            return 0

    def __len__(self):
        return len(self.grades)

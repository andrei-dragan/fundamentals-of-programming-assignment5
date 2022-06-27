from src.exceptions.discipline_exceptions import DisciplineNameException, DisciplineIDException
from src.exceptions.student_exceptions import StudentIDException, StudentNameException
from src.services.student_service import StudentService
from src.services.grade_service import GradeService, GradeException
from src.services.discipline_service import DisciplineService
from src.services.undo_service import UndoException


class UI:
    def __init__(self, student_repo, discipline_repo, grade_repo, undo_service):
        self.__student_repo = student_repo
        self.__discipline_repo = discipline_repo
        self.__grade_repo = grade_repo

        self.__students = StudentService(self.__student_repo, self.__grade_repo, undo_service)
        self.__disciplines = DisciplineService(self.__discipline_repo, self.__grade_repo, undo_service)
        self.__grades = GradeService(self.__grade_repo, self.__student_repo, self.__discipline_repo, undo_service)
        self.__undo = undo_service

    @staticmethod
    def __print_menu():
        print('\n-------------------------------------------------------------------------------------')
        print('\tChoose your command:')
        print('\tType <student add / remove / update / list / search> to perform an action on students.')
        print('\tType <discipline add / remove / update / list / search> to perform an action on disciplines.')

        print('\t')
        print('\tType <stat failed> to display all students failing at one or more disciplines')
        print('\tType <stat students> to display students sorted in descending order of their aggregated average')
        print('\tType <stat disciplines> to display disciplines sorted in descending order of the average grade')
        print('\t')

        print('\t')
        print('\tType <undo / redo op> to perform and undo / redo')
        print('\t')

        print('\tType <grade add / list > to perform an action on grades.')
        print('\tType <exit program> to exit.')
        print('-------------------------------------------------------------------------------------\n')

    def start(self):
        if len(self.__student_repo) == 0:
            self.__students.generate_students(20)
            self.__disciplines.generate_disciplines(20)
            self.__grades.generate_grades(20)

        while True:
            try:
                self.__print_menu()

                commands = input("Type your command: ").split()
                if len(commands) != 2:
                    raise CommandException

                for i in range(len(commands)):
                    commands[i].strip()
                    commands[i] = commands[i].lower()

                if commands[0] == 'student':
                    if commands[1] == 'add':
                        student_id = input("Enter the id of the student: ").strip()
                        name = input("Enter the name of the student: ").strip()
                        self.__students.add(student_id, name)

                    elif commands[1] == 'remove':
                        student_id = input("Enter the id of the student that will be deleted: ").strip()
                        self.__students.remove(student_id)

                    elif commands[1] == 'update':
                        student_id = input("Enter the id of the student to be updated: ").strip()
                        name = input("Enter the updated name of the student: ").strip()
                        self.__students.update(student_id, name)

                    elif commands[1] == 'list':
                        answer = ''
                        students = self.__students.list()
                        for student in students:
                            answer = answer + "student " + str(student[0]) + ": " + str(student[1]) + '\n'
                        print(answer)

                    elif commands[1] == 'search':
                        search_input = input('Insert the ID or the name your are looking for: ').strip()
                        filtered_students = self.__students.search(search_input)
                        for student in filtered_students:
                            print(str(student))

                        if len(filtered_students) == 0:
                            print('We could not find any match!')

                    else:
                        raise CommandException


                elif commands[0] == 'discipline':
                    if commands[1] == 'add':
                        discipline_id = input("Enter the id of the discipline: ").strip()
                        name = input("Enter the name of the discipline: ").strip()
                        self.__disciplines.add(discipline_id, name)

                    elif commands[1] == 'remove':
                        discipline_id = input("Enter the id of the discipline that will be deleted: ").strip()
                        self.__disciplines.remove(discipline_id)

                    elif commands[1] == 'update':
                        discipline_id = input("Enter the id of the discipline to be updated: ").strip()
                        name = input("Enter the updated name of the discipline: ").strip()
                        self.__disciplines.update(discipline_id, name)

                    elif commands[1] == 'list':
                        answer = ''
                        disciplines = self.__disciplines.list()
                        for discipline in disciplines:
                            answer = answer + "discipline " + str(discipline[0]) + ": " + str(discipline[1]) + '\n'
                        print(answer)

                    elif commands[1] == 'search':
                        search_input = input('Insert the ID or the name your are looking for: ').strip()
                        filtered_disciplines = self.__disciplines.search(search_input)
                        for discipline in filtered_disciplines:
                            print(str(discipline))

                        if len(filtered_disciplines) == 0:
                            print('We could not find any match!')

                    else:
                        raise CommandException

                elif commands[0] == 'grade':
                    if commands[1] == 'add':
                        discipline_id = input("Enter the id of the discipline: ").strip()
                        student_id = input("Enter the id of the student: ").strip()
                        grade_value = input("Enter the value of the grade: ").strip()

                        if not self.__students.check_id(student_id):
                            print("There is no student with such ID!")
                        elif not self.__disciplines.check_id(discipline_id):
                            print("There is no discipline with such ID!")
                        else:
                            student_id = int(student_id)
                            discipline_id = int(discipline_id)
                            self.__grades.add(discipline_id, student_id, grade_value)

                    elif commands[1] == 'list':
                        grades = self.__grades.list()
                        answer = ''
                        for grade in grades:
                            answer += self.__students[grade[1]] + " obtained at " + \
                                      self.__disciplines[grade[2]] + " " + str(grade[0]) + '\n'
                        print(answer)

                elif commands[0] == 'stat':
                    if commands[1] == 'failed':
                        failed_students = self.__students.failed()
                        answer = ''

                        if len(failed_students) == 0:
                            answer = 'No students failed ... yet!'

                        for failed_student in failed_students:
                            answer += 'Student ' + str(failed_student) + '-'
                            answer += self.__students[failed_student] + ' failed at: '
                            for discipline in failed_students[failed_student]:
                                answer += self.__disciplines[discipline] + ', '
                            answer = answer[0:-2]
                            answer += '\n'

                        print(answer)

                    elif commands[1] == 'students':
                        students_and_grades = self.__students.top()
                        for student, grade in students_and_grades:
                            if grade != 0:
                                print('Student ' + str(student) + '-' + self.__students[student] +
                                      ' has an average of ' + str(round(grade, 2)))
                            else:
                                print('No grades assigned to student ' + str(student) + '-' + self.__students[student])

                    elif commands[1] == 'disciplines':
                        disciplines_and_grades = self.__disciplines.top()
                        for discipline, grade in disciplines_and_grades:
                            print('Discipline ' + str(discipline) + '-' + self.__disciplines[discipline] +
                                  ' has an average of ' + str(round(grade, 2)))

                    else:
                        raise CommandException

                elif commands[0] == 'exit' and commands[1] == 'program':
                    return

                elif commands[0] == 'undo' and commands[1] == 'op':
                    self.__undo.undo()

                elif commands[0] == 'redo' and commands[1] == 'op':
                    self.__undo.redo()

                else:
                    raise CommandException

            except CommandException:
                print("Invalid Command")
            except StudentIDException as error_message:
                print(error_message)
            except StudentNameException as error_message:
                print(error_message)
            except DisciplineIDException as error_message:
                print(error_message)
            except DisciplineNameException as error_message:
                print(error_message)
            except GradeException as error_message:
                print(error_message)
            except UndoException as error_message:
                print(error_message)


class CommandException(Exception):
    pass

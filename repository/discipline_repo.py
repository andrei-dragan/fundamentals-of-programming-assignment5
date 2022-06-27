from src.domain.discipline.discipline import Discipline
from src.exceptions.discipline_exceptions import DisciplineIDException, DisciplineNameException


class DisciplineRepository:
    def __init__(self):
        self.__disciplines = list()

    @property
    def disciplines(self):
        return self.__disciplines

    @disciplines.setter
    def disciplines(self, disciplines):
        self.__disciplines = disciplines

    def check_id(self, discipline_id):
        """
        Check if there is a discipline with the id of discipline_id
        :param discipline_id: The id of the discipline
        :return: True if there is a discipline with the id of discipline_id, False otherwise
        """
        for discipline in self.disciplines:
            if discipline.id == discipline_id:
                return True
        return False

    def check_name(self, discipline_name):
        """
        Check if there is a discipline with the name of discipline_name
        :param discipline_name: The name of the discipline
        :return: True if there is a discipline with the name of discipline_name, False otherwise
        """
        for discipline in self.disciplines:
            if discipline.name == discipline_name:
                return True
        return False

    def add(self, discipline_id, discipline_name):
        """
        Add a discipline to the list of disciplines after validating the uniqueness of the id and name
        and creating the object discipline, based on the id and name
        :param discipline_id: The id of the discipline we want to add
        :param discipline_name: The name of the discipline we want to add
        :return: None
        """
        if self.check_id(discipline_id):
            raise DisciplineIDException("A discipline with this ID already exists!")

        if self.check_name(discipline_name):
            raise DisciplineNameException("A discipline with this name already exists!")

        discipline = Discipline(discipline_id, discipline_name)
        self.disciplines.append(discipline)

    def remove(self, discipline_id):
        """
        Remove the discipline from the list of disciplines, if it exists
        :param discipline_id: The id of the discipline we want to remove
        :return: The discipline object that was deleted
        """
        if not self.check_id(discipline_id):
            raise DisciplineIDException("A discipline with this ID does not exist!")

        for discipline in self.disciplines:
            if discipline.id == discipline_id:
                self.disciplines.remove(discipline)
                return discipline

    def update(self, discipline_id, discipline_name):
        """
        Update the name of a discipline, if the discipline exists in the list of disciplines and there is no other
        discipline with the same new name
        :param discipline_id: The unique id of the discipline
        :param discipline_name: The updated name of the discipline
        :return: None
        """
        if not self.check_id(discipline_id):
            raise DisciplineIDException("A discipline with this ID does not exist!")

        if self.check_name(discipline_name):
            raise DisciplineNameException("A discipline with this name already exists!")

        for discipline in self.disciplines:
            if discipline.id == discipline_id:
                discipline.name = discipline_name

    def __len__(self):
        return len(self.disciplines)

    def __getitem__(self, discipline_id):
        if self.check_id(discipline_id) is False:
            raise DisciplineIDException("A discipline with this ID does not exist!")

        for discipline in self.disciplines:
            if discipline.id == discipline_id:
                return discipline.name

    def list(self):
        """
        Return a list of tuples representing the id and name of each discipline
        :return: A list of tuples (discipline_id, discipline_name)
        """
        answer = list()
        for discipline in self.disciplines:
            answer.append((discipline.id, discipline.name))
        return answer

    def search(self, search_input):
        """
        Filter the disciplines such that the user's input is (partially) matching the id / name
        :param search_input: The user's input
        :return: A list of matching disciplines
        """
        filtered_disciplines = list()
        for discipline in self.disciplines:
            discipline_id = str(discipline.id).lower()
            discipline_name = str(discipline.name).lower()
            if search_input in discipline_id or search_input in discipline_name:
                filtered_disciplines.append(discipline)
        return filtered_disciplines

    def get_ids(self):
        ids = list()
        for discipline in self.disciplines:
            ids.append(discipline.id)
        return ids

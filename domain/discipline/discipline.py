class Discipline:
    def __init__(self, discipline_id, name):
        self.__discipline_id = discipline_id
        self.__name = name

    @property
    def id(self):
        return self.__discipline_id

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, new_name):
        self.__name = new_name

    def __str__(self):
        return "discipline " + str(self.id) + ": " + str(self.name)

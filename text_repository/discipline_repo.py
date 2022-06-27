from src.repository.discipline_repo import DisciplineRepository


class DisciplineTextFileRepository(DisciplineRepository):
    def __init__(self):
        super().__init__()
        self.__file_name = 'txt_files/disciplines.txt'
        self.__load_file()

    def __load_file(self):
        f = open(self.__file_name, "rt")
        for line in f.readlines():
            discipline_id, discipline_name = line.split(maxsplit=1, sep=' ')
            self.add(int(discipline_id.strip()), discipline_name.strip())
        f.close()

    def __save_file(self):
        f = open(self.__file_name, "wt")

        for discipline in self.disciplines:
            f.write(str(discipline.id) + ' ' + discipline.name + '\n')

        f.close()

    def add(self, discipline_id, discipline_name):
        super(DisciplineTextFileRepository, self).add(discipline_id, discipline_name)
        self.__save_file()

    def update(self, discipline_id, discipline_name):
        super(DisciplineTextFileRepository, self).update(discipline_id, discipline_name)
        self.__save_file()

    def remove(self, discipline_id):
        deleted_discipline = super(DisciplineTextFileRepository, self).remove(discipline_id)
        self.__save_file()
        return deleted_discipline

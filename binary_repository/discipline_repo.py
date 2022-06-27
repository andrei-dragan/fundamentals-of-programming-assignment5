import pickle

from src.repository.discipline_repo import DisciplineRepository


class DisciplineBinaryFileRepository(DisciplineRepository):
    def __init__(self):
        super().__init__()
        self.__file_name = 'binary_files/disciplines.bin'
        self.__load_file()

    def __load_file(self):
        f = open(self.__file_name, "rb")
        self.disciplines = pickle.load(f)
        f.close()

    def __save_file(self):
        f = open(self.__file_name, "wb")
        pickle.dump(self.disciplines, f)
        f.close()

    def add(self, discipline_id, discipline_name):
        super(DisciplineBinaryFileRepository, self).add(discipline_id, discipline_name)
        self.__save_file()

    def update(self, discipline_id, discipline_name):
        super(DisciplineBinaryFileRepository, self).update(discipline_id, discipline_name)
        self.__save_file()

    def remove(self, discipline_id):
        deleted_discipline = super(DisciplineBinaryFileRepository, self).remove(discipline_id)
        self.__save_file()
        return deleted_discipline

import json
from abc import ABC, abstractmethod


class VacancyManager(ABC):
    """ абстрактный класс для работы с полученными вакансиями """

    @abstractmethod
    def _save_vacancies(self) -> None:
        """ Запись данных в файл """
        pass

    @abstractmethod
    def delete_vacancies(self, user_id: str) -> None:
        """ Удаление данных из файла по id """
        pass

    @abstractmethod
    def adding_data(self) -> None:
        """ Добавление вакансий в существующий файл """
        pass


class ReadWriteFile(VacancyManager):
    """ Чтение и записб вакансий в json-файл """
    def __init__(self, data: list) -> None:
        self.data = data

    def _save_vacancies(self) -> None:
        """ Запись списка вакансий в файл json """
        with open('Vacancies_for_you.json', 'w', encoding='utf-8') as file:
            json.dump(self.data, file, ensure_ascii=False, indent=2)

    def delete_vacancies(self, user_id: str) -> None:
        """ Удаление вакансии по id """
        try:
            initial_data = json.load(open("Vacancies_for_you.json", encoding=('utf-8')))
            new_list = [vacancy for vacancy in initial_data if vacancy.get('id') != user_id]
            with open("Vacancies_for_you.json", 'w', encoding='utf-8') as file:
                json.dump(new_list, file, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка: {e}")

    def adding_data(self) -> None:
        """ Добавление вакансий к списку в файле json """
        try:
            initial_data = json.load(open("Vacancies_for_you.json", encoding=('utf-8')))
            new_list = initial_data + self.data
            with open("Vacancies_for_you.json", 'w', encoding='utf-8') as file:
                json.dump(new_list, file, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка: {e}")

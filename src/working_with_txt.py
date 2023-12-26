from abc import ABC, abstractmethod
from typing import Any


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
    def adding_data(self, new_vacansy: Any) -> None:
        """ Добавление вакансий в существующий файл """
        pass


class ReadWriteFile(VacancyManager):
    """ Чтение и запись вакансий в json-файл """
    def __init__(self, data: list) -> None:
        self.data = data

    def _save_vacancies(self) -> None:
        """ Запись списка вакансий в файл json """
        with open('vacancies_for_tou.txt', 'w', encoding='utf-8') as f:
            f.write(str(self.data))

    def delete_vacancies(self, user_id: str) -> None:
        """ Удаление вакансии по id """
        try:
            new_data = [vacancies for vacancies in self.data if vacancies['id'] != user_id]
            with open('vacancies_for_tou.txt', 'w', encoding='utf-8') as f:
                f.write(str(new_data))
        except Exception as e:
            print(f"Ошибка: {e}")

    def adding_data(self, new_vacansy: Any) -> None:
        """ Добавление вакансий к списку в файле json """
        try:
            with open('vacancies_for_tou.txt', 'a', encoding='utf-8') as f:
                f.write(str(new_vacansy))
        except Exception as e:
            print(f"Ошибка: {e}")

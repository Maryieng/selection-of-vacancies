from abc import ABC, abstractmethod
from typing import Any

import pandas as pd


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
    """ Чтение и записб вакансий в json-файл """
    def __init__(self, data: list) -> None:
        self.data = data

    def _save_vacancies(self) -> None:
        """ Запись списка вакансий в файл json """
        df = pd.DataFrame(self.data)
        df.to_excel('./Vacancies_for_you.xlsx')

    def delete_vacancies(self, user_id: str) -> None:
        """ Удаление вакансии по id """
        try:
            df = pd.read_excel('Vacancies_for_you.xlsx')
            df = df[df['id'] != user_id]
            df.to_excel('Vacancies_for_you.xlsx', index=False)
        except Exception as e:
            print(f"Ошибка: {e}")

    def adding_data(self, new_vacansy: Any) -> None:
        """ Добавление вакансий к списку в файле json """
        try:
            new_data = pd.DataFrame(new_vacansy)
            df = pd.read_excel('Vacancies_for_you.xlsx')
            df = pd.concat([df, new_data], axis=1)
            df.to_excel('Vacancies_for_you.xlsx', index=False)
        except Exception as e:
            print(f"Ошибка: {e}")

import csv
from abc import ABC, abstractmethod
from typing import Any

import pandas as pd


class VacancyManager(ABC):
    """ Абстрактный класс для работы с полученными вакансиями """

    @abstractmethod
    def _save_vacancies(self) -> None:
        """ Запись данных в файл """
        pass

    @abstractmethod
    def delete_vacancies(self, user_id: str) -> None:
        """ Удаление данных из файла по id """
        pass

    @abstractmethod
    def adding_data(self, new_vacancy: Any) -> None:
        """ Добавление вакансий в существующий файл """
        pass


class ReadWriteFile(VacancyManager):
    """ Чтение и запись вакансий в csv-файл """
    def __init__(self, data: list) -> None:
        self.data = data

    def _save_vacancies(self) -> None:
        """ Запись списка вакансий в файл csv """
        with open('job_listings.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(self.data)

    def delete_vacancies(self, user_id: str) -> None:
        """ Удаление вакансии по id """
        try:
            df = pd.read_csv('job_listings.csv')
            new_data = [vacansy for vacansy in df if user_id not in vacansy]
            with open('job_listings.csv', 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(new_data)
        except Exception as e:
            print(f"Ошибка: {e}")

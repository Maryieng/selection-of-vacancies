import json
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any
import os
from dotenv import load_dotenv
import requests
load_dotenv()


class VacancyAPI(ABC):
    """ абстрактный класс для работы с API сайтов с вакансиями """

    @abstractmethod
    def connect_get_vacancies(self):
        pass


class VakancyParams:
    """ Параметры для поисков вакансий """
    def __init__(self, vakancy_name: str, sorting: Any, payment_from: int, no_agreement: int):
        self.vakancy_name = vakancy_name
        self.sorting = sorting  # фильтр по дате или сумме publication_time /  salary_desc
        self.payment_from = payment_from  # сумма от
        self.no_agreement = no_agreement  # убрать вакансии без указания оклада (1)

    def __repr__(self):
        """ Вывод введенной вакансии """
        return f'{self.vakancy_name}'


class VacancyManager(ABC):
    """ абстрактный класс для работы с полученными вакансиями """

    @abstractmethod
    def _save_vacancies(self):
        """ Запись данных в файл """
        pass

    @abstractmethod
    def delete_vacancies(self, user_id):
        """ Удаление данных из файла по id """
        pass

    @abstractmethod
    def adding_data(self):
        """ Добавление вакансий в существующий файл """
        pass


class SuperJobAPI(VakancyParams, VacancyAPI):
    """ Класс для получения вакансий с сайта Superjob по критериям пользователя """

    def __init__(self, vakancy_name: str, sorting: str, payment_from: int, no_agreement: int) -> None:
        """ Инициализация """
        super().__init__(vakancy_name, sorting, payment_from, no_agreement)
        self.headers = {'X-Api-App-Id': os.getenv('API_KEY')}
        self.url = f'https://api.superjob.ru/2.0/vacancies'


    def connect_get_vacancies(self) -> Any:
        """ Реализация подключения к API Superjob и получение данных в json формате """
        try:
            response = requests.get(self.url, headers=self.headers,
                                    params={'keywords': self.vakancy_name, 'order_field': self.sorting,
                                            'payment_from': self.payment_from,
                                            'no_agreement': self.no_agreement,
                                            'count': 100}).json()
            return response
        except Exception as e:
            print(f"Ошибка: {e}")

    def load_vacancy(self):
        """ Цикл по словарюю берем из словаря только нужные нам данные и записываем их в переменную 'vacancies_in_SJ' """
        data = self.connect_get_vacancies()
        vacancies_in_SJ = []
        try:
            for vacancy in data['objects']:
                published_at = datetime.fromtimestamp(vacancy.get('date_published', ''))
                super_job = {
                    'id': vacancy['id'],
                    'name': vacancy.get('profession', ''),
                    'solary_ot': vacancy.get('payment_from', '') if vacancy.get('payment_from') else None,
                    'solary_do': vacancy.get('payment_to') if vacancy.get('payment_to') else None,
                    'responsibility': vacancy.get('candidat').replace('\n', '').replace('•', '')
                    if vacancy.get('candidat') else None,
                    'data': published_at.strftime("%d.%m.%Y"),
                    'link': vacancy.get('link') if vacancy.get('link') else None
                }
                vacancies_in_SJ.append(super_job)
            return vacancies_in_SJ
        except Exception as e:
            print(f"Ошибка: {e}")
            return []


class HeadHunterAPI(VakancyParams, VacancyAPI):
    """ Класс для получения вакансий с сайта HeadHunter по критериям пользователя"""

    def __init__(self, vakancy_name: str, sorting: str, payment_from: int, no_agreement: int) -> None:
        """ Инициализация """
        super().__init__(vakancy_name, sorting, payment_from, no_agreement)
        self.base_url = 'https://api.hh.ru/vacancies'

    def connect_get_vacancies(self) -> Any:
        """ Реализация подключения к API HeadHunter и получение данных в json формате """
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                                     ' (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
            response = requests.get(self.base_url, headers=headers,
                                    params={'text': self.vakancy_name, 'order_by': self.sorting,
                                            'salary': self.payment_from, 'only_with_salary': self.no_agreement,
                                            'per_page': 100}).json()
            return response
        except Exception as e:
            print(f"Ошибка: {e}")

    def load_vacancy(self):
        """ Создание списка вакансий с нужными данными """
        data = self.connect_get_vacancies()
        vacancies_in_HH = []
        try:
            for vacancy in data.get('items', []):
                published_at = datetime.strptime(vacancy['published_at'], "%Y-%m-%dT%H:%M:%S%z")
                vacancy_info = {
                    'id': vacancy['id'],
                    'name': vacancy['name'],
                    'solary_ot': vacancy['salary']['from'] if vacancy.get('salary') else None,
                    'solary_do': vacancy['salary']['to'] if vacancy.get('salary') else None,
                    'responsibility': vacancy['snippet']['responsibility'],
                    'data': published_at.strftime("%d.%m.%Y"),
                    'link': vacancy.get('alternate_url') if vacancy.get('alternate_url') else None
                }
                vacancies_in_HH.append(vacancy_info)
            return vacancies_in_HH
        except Exception as e:
            print(f"Ошибка: {e}")


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

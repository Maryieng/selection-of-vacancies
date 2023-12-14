import json
from abc import ABC, abstractmethod
from datetime import datetime
from pprint import pprint
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
    def __init__(self, vakancy_name: str, sorting: int, payment_from: int, no_agreement: int):
        self.vakancy_name = vakancy_name
        self.sorting = sorting  # фильтр по дате или сумме publication_time /  salary_desc
        self.payment_from = payment_from  # сумма от
        self.no_agreement = no_agreement  # убрать вакансии без указания оклада (1)

    def __repr__(self):
        """ Вывод введенной вакансии """
        return f'{self.vakancy_name}'


class SuperJobAPI(VakancyParams, VacancyAPI):
    """ Класс для получения вакансий с сайта Superjob по критериям пользователя """

    def __init__(self, vakancy_name: str, sorting: int, payment_from: int, no_agreement: int) -> None:
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
                                            'no_agreement': self.no_agreement}).json()
            return response
        except Exception as e:
            print(f"Ошибка: {e}")

    def load_vacancy(self):
        """Проходим циклом по словарю берем из словаря только нужные нам данные и записываем их в переменную 'vacancy_list_SJ' """
        data = self.connect_get_vacancies()
        vacancies_in_SJ = []
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


class HeadHunterAPI(VakancyParams, VacancyAPI):
    """ Класс для получения вакансий с сайта HeadHunter по критериям пользователя"""

    def __init__(self, vakancy_name: str, sorting: int, payment_from: int, no_agreement: int) -> None:
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
                                            'salary': self.payment_from, 'only_with_salary': self.no_agreement}).json()
            return response
        except Exception as e:
            print(f"Ошибка: {e}")

    def load_vacancy(self):
        """ Создание списка вакансий с нужными данными """
        data = self.connect_get_vacancies()
        vacancies_in_HH = []
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


class WriteToFile:
    def __init__(self, data: list) -> None:
        self.data = data

    def write_to_file(self) -> None:
        with open('Vacancies_for_you', 'w', encoding='utf-8') as file:
            json.dump(self.data, file, ensure_ascii=False, indent=2)


# api = HeadHunterAPI('разработчик', 'publication_time', 50000, 1)
# new_class = WriteToFile(api.load_vacancy())
# new_class.write_to_file()
# pprint(api.load_vacancy())
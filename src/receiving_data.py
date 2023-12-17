import os
from abc import ABC, abstractmethod
from typing import Any

import requests
from dotenv import load_dotenv

load_dotenv()


class VacancyAPI(ABC):
    """ абстрактный класс для работы с API сайтов с вакансиями """

    @abstractmethod
    def connect_get_vacancies(self) -> Any:
        pass


class VakancyParams:
    """ Параметры для поисков вакансий """
    def __init__(self, vakancy_name: str, sorting: Any, payment_from: int, no_agreement: int):
        self.vakancy_name = vakancy_name
        self.sorting = sorting  # фильтр по дате или сумме publication_time /  salary_desc
        self.payment_from = payment_from  # сумма от
        self.no_agreement = no_agreement  # убрать вакансии без указания оклада (1)

    def __repr__(self) -> str:
        """ Вывод введенной вакансии """
        return f'{self.vakancy_name}'


class SuperJobAPI(VakancyParams, VacancyAPI):
    """ Класс для получения вакансий с сайта Superjob по критериям пользователя """

    def __init__(self, vakancy_name: str, sorting: str, payment_from: int, no_agreement: int) -> None:
        """ Инициализация """
        super().__init__(vakancy_name, sorting, payment_from, no_agreement)
        self.headers = {'X-Api-App-Id': os.getenv('API_KEY')}
        self.url = 'https://api.superjob.ru/2.0/vacancies'

    def connect_get_vacancies(self) -> Any:
        """ Реализация подключения к API Superjob и получение данных в json формате """
        try:
            response = requests.get(self.url, headers=self.headers,  # type: ignore
                                    params={'keywords': self.vakancy_name, 'order_field': self.sorting,
                                            'payment_from': self.payment_from,
                                            'no_agreement': self.no_agreement,
                                            'count': 100}).json()
            return response
        except Exception as e:
            print(f"Ошибка: {e}")


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

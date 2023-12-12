from abc import ABC, abstractmethod
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


class SuperjobAPI(VacancyAPI):
    """ Класс для получения вакансий с сайта Superjob """

    def __init__(self) -> None:
        """ Инициализация """
        self.headers = {'X-Api-App-Id': os.getenv('API_KEY')}
        self.superjob_url = f'https://api.superjob.ru/2.0/vacancies'

    def connect_get_vacancies(self) -> Any:
        """ Реализация подключения к API Superjob и получение данных в json формате """
        try:
            response = requests.get(self.superjob_url, headers=self.headers)
            return response.json()
        except Exception as e:
            print(f"Ошибка подключения: {e}")


class HeadHunterAPI(VacancyAPI):
    """ Класс для получения вакансий с сайта HeadHunter """

    def __init__(self) -> None:
        """ Инициализация """
        self.base_url = 'https://api.hh.ru/vacancies'

    def connect_get_vacancies(self) -> Any:
        """ Реализация подключения к API HeadHunter и получение данных в json формате """
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                                     ' (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
            response = requests.get(self.base_url, headers=headers)
            return response.json()
        except Exception as e:
            print(f"Ошибка подключения: {e}")


api = SuperjobAPI()
pprint(api.connect_get_vacancies())

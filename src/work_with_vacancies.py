from datetime import datetime
from typing import Any


class DataValidation:

    def __init__(self, response: Any) -> None:
        self.response = response

    def load_vacancy_sj(self) -> list:
        """ Цикл по словарюю берем из словаря только нужные нам данные и записываем их в переменную 'vacancies_in_SJ'
        """
        vacancies = []
        try:
            for vacancy in self.response['objects']:
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
                vacancies.append(super_job)
            return vacancies
        except Exception as e:
            print(f"Ошибка: {e}")
            return []

    def load_vacancy_hh(self) -> Any:
        """ Создание списка вакансий с нужными данными """
        vacancies = []
        try:
            for vacancy in self.response.get('items'):
                published_at = datetime.strptime(vacancy['published_at'], "%Y-%m-%dT%H:%M:%S%z")
                vacancy_info = {
                    'id': vacancy['id'],
                    'name': vacancy['name'],
                    'solary_ot': vacancy['salary']['from'] if vacancy.get('salary') else None,
                    'solary_do': vacancy['salary']['to'] if vacancy.get('salary') else None,
                    'responsibility': vacancy['snippet']['responsibility'],
                    'data': published_at.strftime("%d.%m.%Y"),
                    'link': vacancy['alternate_url'] if vacancy.get('alternate_url') else None
                }
                vacancies.append(vacancy_info)
            return vacancies
        except Exception as e:
            print(f"Ошибка: {e}")

    @staticmethod
    def get_top_vacancies(vacancies: list) -> list:
        top_5_vacancies = sorted(vacancies, key=lambda x: x.get('salary', {}).get('from', 0), reverse=True)[:5]
        return top_5_vacancies

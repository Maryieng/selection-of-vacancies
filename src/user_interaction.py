from src.getting_vacancies import SuperJobAPI, HeadHunterAPI, ReadWriteFile


def receiving_data_from_the_user():
    while True:
        platforms = input("""Выберете цифру для поиска:
        1 - HeadHunter 
        2 - SuperJob
        """)
        vakancy_name = input("""Укажите профессию
        """)
        payment_from = int(input("""Укажите минимальную желаемую сумму зарплаты
        """))
        no_agreement = int(input("""Нужно ли выводить вакансии без указания заработной платы (По договоренности)?
        1 - Нет 
        2 - Да
        """))
        sorting = input("""Укажите сортировку: Дата/Зарплата
        """).lower()

        if platforms == '1':
            if sorting == "дата":
                sorting = 'publication_time'
            else:
                sorting = 'salary_desc'
            activation_class = HeadHunterAPI(vakancy_name, sorting, payment_from, no_agreement)
        else:
            if sorting == "дата":
                sorting = 'date'
            else:
                sorting = 'payment'
            activation_class = SuperJobAPI(vakancy_name, sorting, payment_from, no_agreement)

        vacancy_data = activation_class.load_vacancy()
        activating_class_for_record = ReadWriteFile(vacancy_data)

        data_status = input("""Выберите действие:
        1. Создать новый файл 
        2. Дополнить прежний (при условии уже выполненого ранее 1 пункта)
        """)
        if data_status == '1':
            activating_class_for_record._save_vacancies()
            print("Файл создан успешно")
        else:
            activating_class_for_record.adding_data()
            print("Файл дополнен успешно")
        while True:
            choice_to_delete = input('''Хотите удалить какую-либо вакансию из файла? Да/Нет
            ''').lower()
            if choice_to_delete == "да":
                vacancy_for_removal = input("""Введите id вакансии для удаления
                """)
                activating_class_for_record.delete_vacancies(vacancy_for_removal)
                print("Успешно удалено")
            else:
                break
        continuation_of_the_cycle = input("""Хотите повторно сформировать список подходящих вакансий? Да/Нет
        """).lower()
        if continuation_of_the_cycle == "нет":
            break


receiving_data_from_the_user()

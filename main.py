import requests
import datetime
import os

# Обозначаем константы
TODOS = 'https://json.medrating.org/todos'
USERS = 'https://json.medrating.org/users'


# Создание собственного словаря на основание данных константы TODOS
def get_todos_dict(api_todos):
    result_id = {}
    for i in api_todos(TODOS):
        try:
            dict_users = {i['id']: [i['userId'], i['title'], i['completed']]}
            result_id.update(dict_users)
        except KeyError as error:
            print(f'Пустой {error.args} в {TODOS}')
    return result_id


# Создание собственного словаря на основание данных константы USERS
def get_users_dict(api_user):
    result = {}
    for i in api_user(USERS):
        try:
            dict_users = {i['id']: [i['name'], i['email'], i['company']['name']]}
            result.update(dict_users)
        except KeyError as error:
            print(f'Пустой {error.args} в {USERS}')
    return result


# Получение данных для словаря на основание их константы TODOS
@get_todos_dict
def api_todos(cons_todos):
    todos = requests.get(cons_todos)
    return todos.json()


# Получение данных для словаря на основание их константы USERS
@get_users_dict
def api_user(cons_users):
    to = requests.get(cons_users)
    return to.json()


# Проверять если есть директория то пасс если нет то создать
def done_dir(tasks):
    global path_files
    path_files = os.getcwd() + '/' + tasks + '/'

    try:
        os.mkdir(path_files)
        print("Успешно создана директория %s " % path_files)
    except Exception as e:
        if e.strerror == 'File exists':
            print(f'Директория {path_files} уже создана')


def processing(id_u, name_u, email_u, company_u):
    """
    Основная функция для генерации отчетов. Здесь мы выполняем основные условия задачи:
    1) get_todos_dict - словарь с данными о результате User
    2) get_users_dict - словарь с данными о соамом User
    Основная работа проводиться с get_todos_dict собраные даммы мы прикремляем к get_users_dict и создаем свои поля
    для передачи в отчет.
    :param id_u: Передаем ID для определения User
    :param name_u: Передаем Имя юзера
    :param email_u: Передаем Почту юзера
    :param company_u: Передаем Компанию юзера
    :return: Получаю сгенерированые файлы(отчеты) по каждому юзеру
    """
    # подсчет завершенных и незавершенных задач

    count_task_true = 0
    count_task_false = 0

    # сбор названий завершенных и незавершенных задач
    list_title_close_task = []
    list_title_open_task = []

    for ds in api_todos.keys():
        if api_todos[ds][0] == id_u:
            if api_todos[ds][2] == False:
                count_task_false += 1

        if api_todos[ds][0] == id_u:
            if api_todos[ds][2] == True:
                count_task_true += 1

        if api_todos[ds][0] == id_u:
            if api_todos[ds][2] == True:
                if len(api_todos[ds][1]) > 48:
                    list_title_close_task.append(api_todos[ds][1][0:45] + '...')
                else:
                    list_title_close_task.append(api_todos[ds][1])

        if api_todos[ds][0] == id_u:
            if api_todos[ds][2] == False:
                if len(api_todos[ds][1]) > 48:
                    list_title_open_task.append(api_todos[ds][1][0:45] + '...')
                else:
                    list_title_open_task.append(api_todos[ds][1])

    # Определяем местное время и интервал создания файлов
    offset = datetime.timezone(datetime.timedelta(hours=3))
    today = datetime.datetime.now(offset)
    time_for_write = today.strftime("%d.%m.%Y %H:%M")  # ДД.ММ.ГГ ЧЧ:ММ



    # Если запущена повторная генерация отчетов, то переименовываем файлы(отчеты) если они устарели.
    try:

        # Получаем дату модификации файла
        data_update_file = os.path.getmtime(path_files + name_u + ".txt")
        time_for_rename_file = datetime.datetime.fromtimestamp(data_update_file).strftime('%Y-%m-%dT%H:%M')

        old_file = os.path.join(path_files, name_u + ".txt")

        new_file = os.path.join(path_files, 'old_' + name_u + '_' + time_for_rename_file + ".txt")
        os.rename(old_file, new_file)

    except OSError as e:

        print(f'Файл {e.filename} создается')

    # Проверяем наличие файла отчета
    chek_file = os.path.exists(path_files + name_u)
    if not chek_file:
        #   Путь для создания файлов(отчетов)
        page_done_file_anotation = path_files + name_u + '.txt'

        #  Создание и запись собраных данных в файлы(отчеты)
        with open(page_done_file_anotation, 'w', encoding='UTF-8') as f:
            delimiter_str = '\n'
            title_close_task = delimiter_str.join(list_title_close_task)
            title_open_task = delimiter_str.join(list_title_open_task)

            f.write(name_u + '.' + delimiter_str + \
                    str(company_u) + ' ' + "<" + email_u + "> " + str(time_for_write) + delimiter_str + \
                    "Всего задач: " + str(count_task_true + count_task_false) + delimiter_str + delimiter_str + \
                    "Завершённые задачи (" + str(count_task_true) + ")" + ':' + delimiter_str + str(
                title_close_task) + delimiter_str + \
                    delimiter_str + \
                    "Открытые задачи (" + str(count_task_false) + ")" + ':' + delimiter_str + str(
                title_open_task) + delimiter_str)


# Порядок запуска скрыпта
def run():
    done_dir('tasks')
    for f, k in api_user.items():
        processing(f, k[0], k[1], k[2])


if __name__ == '__main__':
    run()  # Запуск скрипта
    print('Отчеты созданы и добавлены в директорию tasks')
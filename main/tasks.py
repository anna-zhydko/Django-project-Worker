from WorkerApp.celery import app
from .parser_modules import work_ua, rabota_ua, jooble
from .models import Job
from .config import *
import requests
from bs4 import BeautifulSoup
from .utils import check_existence, insert_db
from celery import group


@app.task
def clear_db():
    print('clear')
    Job.objects.all().delete()

# This task gets the info about a vacancy from work.ua and inserts it to db
@app.task
def work_ua_insert():
    print('work ua')
    if work_ua.request_successful():
        for page in range(1, work_ua.get_page_count()):
            it_vacancies_html = work_ua.check_limit_exceeded(URL_WORKUA, {'page': page})
            if it_vacancies_html == '':
                break
            if page == 1:
                vacancies_urls = work_ua.get_vacancies_urls(it_vacancies_html, 'div', 'card card-hover card-visited '
                                                                                      'wordwrap job-link js-hot-block')
            else:
                vacancies_urls = work_ua.get_vacancies_urls(it_vacancies_html, 'div',
                                                            'card card-hover card-visited wordwrap job-link')
            vacancies_info = work_ua.get_vacancies_info(vacancies_urls)
            for vacancy_info in vacancies_info:
                if check_existence(vacancy_info['title'], vacancy_info['company_name'], vacancy_info['city']) is False:
                    insert_db(vacancy_info)
                    print(vacancy_info['title'], vacancy_info['company_name'], vacancy_info['city'])
    print('Work_ua. The end')


# This task gets the info about a vacancy via rabota.ua API and inserts it to db
@app.task
def rabota_ua_insert():
    if rabota_ua.request_successful():
        print('rabota ua')
        # Minus 2 for insurance
        for page in range(1, rabota_ua.get_page_count() - 2):
            vacancies = rabota_ua.check_limit_exceeded(VACANCIES_API, {'keyWords': 'programmer', 'page': page})
            if vacancies == '':
                break
            vacancies_id = [vacancy['id'] for vacancy in vacancies['documents']]
            for vacancy_info in rabota_ua.get_vacancies_info(vacancies_id):
                if check_existence(vacancy_info['title'], vacancy_info['company_name'], vacancy_info['city']) is False:
                    insert_db(vacancy_info)
                    print(vacancy_info['title'], vacancy_info['url'])
    print('Rabota_ua. The end')


# This task gets the info about a vacancy from jooble and inserts it to db
@app.task
def jooble_insert():
    print('jooble')
    if jooble.request_successful():
        for page in range(1, jooble.get_page_count()):
            it_vacancies_html = jooble.check_limit_exceeded(URL_JOOBLE, {'page': page})
            if it_vacancies_html == '':
                break
            vacancies_urls = jooble.get_vacancies_urls(it_vacancies_html)
            vacancies_info = jooble.get_vacancies_info(vacancies_urls)
            for vacancy_info in vacancies_info:
                if check_existence(vacancy_info['title'], vacancy_info['company_name'], vacancy_info['city']) is False:
                    insert_db(vacancy_info)
                    print(vacancy_info['title'], vacancy_info['url'])
    print('Jooble_ua. The end')


@app.task
def task_group():
    print('task group')
    return group([clear_db.s(), work_ua_insert.s(), rabota_ua_insert.s(), jooble_insert.s()])
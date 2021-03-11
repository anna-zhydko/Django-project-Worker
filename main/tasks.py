from WorkerApp.celery import app
from .parser_modules import work_ua, rabota_ua, jooble
from .models import Job
from .config import *
import requests
from bs4 import BeautifulSoup
from .utils import check_existence, insert_db, translator
from celery import group


# This task gets the info about a vacancy from work.ua and inserts it to db
@app.task
def work_ua_insert():
    if work_ua.request_successful():
        for page in range(1, work_ua.get_page_count()):
            it_vacancies_html = work_ua.check_limit_exceeded(URL_WORKUA, {'page': page})
            if it_vacancies_html == '':
                print('break')
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
                    print(vacancy_info['title'])


# This task gets the info about a vacancy via rabota.ua API and inserts it to db
@app.task
def rabota_ua_insert():
    if rabota_ua.request_successful():
        # Minus 2 for insurance
        for page in range(1, 2):
            print(page)
            vacancies = rabota_ua.check_limit_exceeded(VACANCIES_API, {'keyWords': 'programmer', 'page': page})
            print('vacancies 1', len(vacancies))
            print('vacancies 2', len(rabota_ua.check_limit_exceeded(VACANCIES_API, {'keyWords': 'programmer'})))
            if vacancies == '':
                break
            vacancies_id = [vacancy['id'] for vacancy in vacancies['documents']]
            for vacancy_info in rabota_ua.get_vacancies_info(vacancies_id):
                if check_existence(vacancy_info['title'], vacancy_info['company_name'], vacancy_info['city']) is False:
                    insert_db(vacancy_info)
                    print(vacancy_info['title'])


# This task gets the info about a vacancy from jooble and inserts it to db
@app.task
def jooble_insert():
    if jooble.request_successful():
        for page in range(1, jooble.get_page_count()):
            it_vacancies_html = jooble.check_limit_exceeded(URL_JOOBLE, {'p': page})
            if it_vacancies_html == '':
                break
            vacancies_urls = jooble.get_vacancies_urls(it_vacancies_html)
            vacancies_info = jooble.get_vacancies_info(vacancies_urls)
            for vacancy_info in vacancies_info:
                if check_existence(vacancy_info['title'], vacancy_info['company_name'], vacancy_info['city']) is False:
                    insert_db(vacancy_info)
                    print(vacancy_info['title'])


@app.task
def all_tasks():
    Job.objects.all().delete()
    task_group = group([work_ua_insert.s(), rabota_ua_insert.s(), jooble_insert.s()])
    task_group()

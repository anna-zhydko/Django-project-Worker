from WorkerApp.celery import app
from .parser_modules import work_ua, rabota_ua, jooble
from .models import Job


# The function checks if the vacancy with the same title, company_name and city already exists in a db - in that case
# the vacancy is not adding to the db
def check_existence(title, company_name, city):
    if not Job.objects.all():
        return False
    for job in Job.objects.all():
        if title == job.title and company_name == job.company_name and city == job.city:
            return True
    return False


# The function inserts a record to db
def insert_db(vacancy_info):
    job = Job(title=vacancy_info['title'], url=vacancy_info['url'],
              company_name=vacancy_info['company_name'],
              city=vacancy_info['city'], salary=vacancy_info['salary'],
              employment=vacancy_info['employment'],
              prog_lang=vacancy_info['prog_lang'], skills=vacancy_info['skills'],
              data_bases=vacancy_info['databases'], description=vacancy_info['description'])
    job.save()


# This task gets the info about a vacancy from work.ua and inserts it to db
@app.task
def work_ua_insert():
    Job.objects.all().delete()
    if work_ua.request_successful():
        for page in range(1, work_ua.get_page_count()):
            it_vacancies_html = work_ua.check_limit_exceeded(work_ua.URL, {'page': page})
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
    print('Work_ua. The end')


# This task gets the info about a vacancy via rabota.ua API and inserts it to db
@app.task
def rabota_ua_insert():
    if rabota_ua.request_successful():
        print('successfull')
        # Minus 2 for insurance
        for page in range(1, rabota_ua.get_page_count() - 2):
            vacancies = rabota_ua.check_limit_exceeded(rabota_ua.VACANCIES_API, {'keyWords': 'programmer', 'page': page})
            vacancies_id = [vacancy['id'] for vacancy in vacancies['documents']]
            for vacancy_info in rabota_ua.get_vacancies_info(vacancies_id):
                if check_existence(vacancy_info['title'], vacancy_info['company_name'], vacancy_info['city']) is False:
                    insert_db(vacancy_info)
    print('Rabota_ua. The end')


# This task gets the info about a vacancy from jooble and inserts it to db
@app.task
def jooble_insert():
    if jooble.request_successful():
        for page in range(1, jooble.get_page_count()):
            it_vacancies_html = jooble.check_limit_exceeded(jooble.URL, {'page': page})
            vacancies_urls = jooble.get_vacancies_urls(it_vacancies_html)
            vacancies_info = jooble.get_vacancies_info(vacancies_urls)
            for vacancy_info in vacancies_info:
                if check_existence(vacancy_info['title'], vacancy_info['company_name'], vacancy_info['city']) is False:
                    insert_db(vacancy_info)
    print('Jooble_ua. The end')

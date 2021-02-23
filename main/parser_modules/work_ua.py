import requests
from bs4 import BeautifulSoup
import re
from ..google_translator import translator
from ..models import Job
from .config import *


proxy_list = []


# get proxies list from website
def get_proxies():
    proxy_url = 'https://www.ip-adress.com/proxy-list'
    response = requests.get(proxy_url).text
    soup = BeautifulSoup(response, 'html.parser')
    return [row.text.split('\n')[1] for row in soup.find('tbody').findAll('tr')]


# The function makes request from website and gets response
def get_response(url, params=None, proxies=None, timeout=None):
    response = requests.get(url, headers=HEADERS, params=params, proxies=proxies, timeout=timeout)
    return response


# if limit is exceeded then makes request via proxy
def check_limit_exceeded(url, params=None):
    try:
        response = get_response(url, params)
        print(response.status_code)
        return response.text
    except:
        print('___________proxy_______________')
        global proxy_list
        if not proxy_list:
            proxy_list = get_proxies()
        print(proxy_list)
        for proxies in proxy_list:
            try:
                print('_________successfull__________________')
                response = get_response(url, params, proxies, 10)
                return response.text
            except:
                print('____________failed_______________')
                pass
    return ''


# The function gets the vacancies urls by parsing via "BeautifulSoup"
def get_vacancies_urls(html, tag, class_):
    soup = BeautifulSoup(html, 'html.parser')
    vacancies_urls = []
    vacancies = soup.find_all(tag, class_=class_)
    for vacancy in vacancies:
        a = vacancy.findChild('a').get('href')
        vacancies_urls.append(HOST_WORKUA + a)
    return vacancies_urls


# The function checks if piece of information exists on page. For example, vacancy could not have a description...
def check_info(vacancy_html, title):
    soup = BeautifulSoup(vacancy_html, 'html.parser')
    try:
        if title == 'Зарплата':
            return soup.find('span', title=title).findParent('p').b.text.replace('\u202f', '').replace('\u2009', '')
        return soup.find('span', title=title).findParent('p').text.strip().replace('\n', '')
    except AttributeError:
        return ''


# Collect the information the vacancies
def get_vacancies_info(vacancies_urls):
    vacancies_info = []
    for vacancy_url in vacancies_urls:
        vacancy_html = check_limit_exceeded(vacancy_url)
        soup = BeautifulSoup(vacancy_html, 'html.parser')
        title = soup.find('h1', id='h1-name')
        employment_type = ' '.join(re.findall(r"\w+ занятость", check_info(vacancy_html, 'Условия и требования'))) + ' '
        remote_work = ' '.join(re.findall(r"[У|у]даленная работа", check_info(vacancy_html, 'Условия и требования')))
        salary = re.findall(r"\d+", check_info(vacancy_html, 'Зарплата'))
        description = soup.find('div', id='job-description')
        description = description.text if description else ''
        vacancy_address = re.findall(r"\w+\b", check_info(vacancy_html, 'Адрес работы'))
        if description:
            databases_list = re.findall(r'mysql|postgresql|nosql|mariadb|sqlite|oracle|mongodb|ms sql',
                                        description.lower())
            prog_lang_list = re.findall(r'|python|c*/*c\+\+|c#|javasript|java|php|typescript|swift|ruby',
                                        description.lower())
            skills_list = re.findall(r'|html|css|\.net|1c|flash|excel|2d|3d|git|tcp/ip|qa|sql', description.lower())
        else:
            databases_list, prog_lang_list, skills_list = '', '', ''
        vacancy_info = {'title': title.text if title else '',
                        'url': vacancy_url,
                        # translate a city to ukrainian
                        'city': translator(vacancy_address[0], 'ru', 'uk') if vacancy_address else '',
                        'company_name': check_info(vacancy_html, 'Данные о компании'),
                        'salary': salary[0] if salary else '',
                        'employment': (employment_type + remote_work),
                        'databases': ' '.join(list(set(databases_list))),  # delete duplicates with set()
                        'prog_lang': ' '.join(list(set(prog_lang_list))),
                        'skills': ' '.join(list(set(skills_list))),
                        'description': description
                        }

        vacancies_info.append(vacancy_info)
    return vacancies_info


# The function returns the number of pages in work_ua that containes the vacancies in IT-sphere
def get_page_count():
    pagination_html = check_limit_exceeded(URL_WORKUA)  # get html from page that contains maximum numbers of pages
    soup = BeautifulSoup(pagination_html, 'html.parser')
    try:
        return int(soup.find('ul', class_='pagination hidden-xs').find_all('li')[-2].text) + 1
    except:
        return 2


# The function checks if request is successful
def request_successful():
    try:
        check_limit_exceeded(URL_WORKUA)
        return True
    except:
        return False









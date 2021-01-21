import requests
from bs4 import BeautifulSoup
import re
from ..google_translator import translator
from ..models import Job


HOST = 'https://ua.jooble.org'
URL = 'https://ua.jooble.org/%D1%80%D0%BE%D0%B1%D0%BE%D1%82%D0%B0-programmer?date=3'
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,'
              '*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/84.0.4147.105 Safari/537.36'

}

# The function receives html data from page
def get_html(url, params=''):
    response = requests.get(url, headers=HEADERS, params=params)
    return response.text

# The function gets the vacancies urls by parsing via "BeautifulSoup"
def get_vacancies_urls(html):
    soup = BeautifulSoup(html, 'html.parser')
    vacancies_urls = []
    vacancies = soup.find_all('div', class_='left-static-block')
    for vacancy in vacancies:
        vacancies_urls.append(vacancy.findChild('a').get('href'))
    return vacancies_urls


# The function checks if piece of information exists on page. For example, vacancy could not have a description...
def check_info(vacancy_html, tag, class_):
    soup = BeautifulSoup(vacancy_html, 'html.parser')
    try:
        return soup.find(tag, class_=class_).text
    except:
        return ''


# The function converts a salary from dollars or euros into uah by using privatbank api
def currency_converter(salary):
    response = requests.get('https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5', headers=HEADERS)
    salary = salary.replace(' ', '')
    if salary[-1] == '$':
        rate = int(float(response.json()[0]['sale']) * int(re.findall(r"\d+", salary)[0]))
    elif salary[-1] == '€':
        rate = int(float(response.json()[0]['sale']) * int(re.findall(r"\d+", salary)[0]))
    else:  # means 'uah'
        rate = int(re.findall(r"\d+", salary)[0])
    return str(rate)


# Collect the information the vacancies
def get_vacancies_info(vacancy_urls):
    vacancies_info = []
    for vacancy_url in vacancy_urls:
        vacancy_html = get_html(vacancy_url)
        salary = check_info(vacancy_html, 'span', 'bb301 h3')
        # translate employment_type and remote_work to russian
        employment_type = translator(check_info(vacancy_html, 'p', '_77a3a d3fee _356ae'), 'uk', 'ru')
        remote_work = translator(check_info(vacancy_html, 'li', '_6748d _1b77c'), 'uk', 'ru')
        if remote_work != 'удаленная работа':
            remote_work = ''
        # translate a city to ukrainian lang
        city = translator(check_info(vacancy_html, 'div', 'caption _584c5'), 'ru', 'uk')
        description = check_info(vacancy_html, 'div', 'a708d')
        if description:
            databases_list = re.findall(r'mysql|postgresql|nosql|mariadb|sqlite|oracle|mongodb|ms sql',
                                        description.lower())
            prog_lang_list = re.findall(r'|python|c*/*c\+\+|c#|javasript|java|php|typescript|swift|ruby',
                                        description.lower())
            skills_list = re.findall(r'|html|css|\.net|1c|flash|excel|2d|3d|git|tcp/ip|qa|sql', description.lower())
        else:
            databases_list, prog_lang_list, skills_list = '', '', ''
        vacancy_info = {'title': check_info(vacancy_html, 'h1', '_65c1a h2'),
                        'url': vacancy_url,
                        'city': city,
                        'company_name': check_info(vacancy_html, 'a', '_786d5 a5cdf'),
                        'salary': currency_converter(salary) if salary != '' else '',
                        'employment': (employment_type + remote_work),
                        'databases': ' '.join(list(set(databases_list))),  # delete duplicates with set()
                        'prog_lang': ' '.join(list(set(prog_lang_list))),
                        'skills': ' '.join(list(set(skills_list))),
                        'description': description
                        }
        vacancies_info.append(vacancy_info)
    return vacancies_info


# The function returns the number of pages in jooble that containes the vacancies in IT-sphere
def get_page_count():
    pagination_html = get_html(URL)  # get html from page that contains maximum numbers of pages
    soup = BeautifulSoup(pagination_html, 'html.parser')
    try:
        # get count of all vacancies in IT-catigory in jooble at the current moment
        results_count = int(re.findall(r"\d*", soup.find('p', id='pResultCount').text.replace(' ', ''))[0]) + 1
        return results_count // 20 - 3 # divide by 20, because one page on jooble.ua containes 20 vacacancies
    except:
        return 1


# The function checks if request is successful
def request_successful():
    response = requests.get(URL, headers=HEADERS)
    if response.status_code == 200:
        return True
    else:
        return False





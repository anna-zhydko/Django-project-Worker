import requests
from bs4 import BeautifulSoup
import re
from ..utils import get_response, get_proxies, translator
from ..config import *
from ..models import Job


proxy_list = []
# if limit is exceeded then makes request via proxy
def check_limit_exceeded(url, params=None):
    try:
        response = get_response(url, params)
        return response.json()
    except:
        global proxy_list
        if not proxy_list:
            proxy_list = get_proxies()
        for proxy in proxy_list:
            try:
                response = get_response(url, params, proxy, 10)
                return response.json()
            except:
                pass
    return ''



# Collect the information the vacancies
def get_vacancies_info(vacancies_id):
    vacancies_info = []
    for vacancy_id in vacancies_id:
        vacancy_json = check_limit_exceeded(VACANCY_API, {'id': vacancy_id})
        if vacancy_json == '':
            break
        employment = [cluster['groups'][0]['name'] if cluster['id'] == 52 else '' for cluster in vacancy_json['clusters']]
        description = BeautifulSoup(vacancy_json['description'], 'html.parser').text
        databases_list = re.findall(r'mysql|postgresql|nosql|mariadb|sqlite|oracle|mongodb|ms sql', description.lower())
        prog_lang_list = re.findall(r'|python|c*/*c\+\+|c#|javasript|java|php|typescript|swift|ruby',
                                    description.lower())
        skills_list = re.findall(r'|html|css|\.net|1c|flash|excel|2d|3d|git|tcp/ip|qa|sql', description.lower())
        vacancy_info = {'title': vacancy_json['name'],
                        'url': 'https://rabota.ua/company{}/vacancy{}'.format(vacancy_json['notebookId'],
                                                                              vacancy_json['id']),
                        'company_name': vacancy_json['companyName'],
                        # Translate a city to ukrainian
                        'city': translator(vacancy_json['cityName'], 'ru', 'uk'),
                        'salary': str(vacancy_json['salary']) if vacancy_json['salary'] != 0 else '',
                        'employment': employment[0] if employment else '',
                        'databases': ' '.join(list(set(databases_list))),  # delete duplicates with set()
                        'prog_lang': ' '.join(list(set(prog_lang_list))),
                        'skills': ' '.join(list(set(skills_list))),
                        'description': description,
                        }
        vacancies_info.append(vacancy_info)
    return vacancies_info


# The function returns the number of pages in rabota.ua that containes the vacancies in IT-sphere
def get_page_count():
    # try:
    #     response = requests.get(URL_RABOTAUA, headers=HEADERS).text
    #     soup = BeautifulSoup(response, 'html.parser')
    #     return int(soup.find('span', class_='f-text-gray f-pagination-ellipsis -right').findParent().a.text)
    # except:
    return 2


# The function checks if request is successful
def request_successful():
    try:
        vacancies = check_limit_exceeded(VACANCIES_API)
        vacancy_id = vacancies['documents'][0]['id']
        check_limit_exceeded(VACANCY_API, {'id': vacancy_id})
        if requests.get(URL_RABOTAUA, headers=HEADERS).status_code == 200:
            return True
        else:
            return False
    except:
        return False






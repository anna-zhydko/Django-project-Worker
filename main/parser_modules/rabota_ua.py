import requests
from bs4 import BeautifulSoup
import re
from ..google_translator import translator
from ..models import Job

HOST = 'https://rabota.ua/'
VACANCIES_API = 'https://api.rabota.ua/vacancy/search'
VACANCY_API = 'https://api.rabota.ua/vacancy'
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'}


# The function returns response in json format because we use rabota.ua API
def get_json(url, params=''):
    response = requests.get(url, headers=HEADERS, params=params)
    return response.json()

# Collect the information the vacancies
def get_vacancies_info(vacancies_id):
    vacancies_info = []
    for vacancy_id in vacancies_id:
        vacancy_json = get_json(VACANCY_API, {'id': vacancy_id})
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
    url = 'https://rabota.ua/zapros/programmer/%d1%83%d0%ba%d1%80%d0%b0%d0%b8%d0%bd%d0%b0'
    response = requests.get(url, headers=HEADERS).text
    soup = BeautifulSoup(response, 'html.parser')
    return int(soup.find('span', class_='f-text-gray f-pagination-ellipsis -right').findParent().a.text)


# The function checks if request is successful
def request_successful():
    try:
        get_json(VACANCIES_API)
        get_json(VACANCY_API)
        return True
    except:
        return False






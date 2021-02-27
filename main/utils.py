from googletrans import Translator
from .models import Job
from .config import *
import requests
from bs4 import BeautifulSoup



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


# The function returns translated text from source lang to destination lang
def translator(text, source, destination):
    translator_object = Translator()
    try:
        return translator_object.translate(text, src=source, dest=destination).text
    except:
        return ''

# The function makes request from website and gets response
def get_response(url, params=None, proxies=None, timeout=None):
    response = requests.get(url, headers=HEADERS, params=params, proxies=proxies, timeout=timeout)
    return response

# get proxies list from website
def get_proxies():
    proxy_url = 'https://www.ip-adress.com/proxy-list'
    response = requests.get(proxy_url).text
    soup = BeautifulSoup(response, 'html.parser')
    return [row.text.split('\n')[1] for row in soup.find('tbody').findAll('tr')]
from django import forms

# The capital cities of the regions
cities = ['All cities', 'Вінниця', 'Дніпро', 'Донецьк', 'Житомир', 'Запоріжжя', 'Івано-Франківськ', 'Київ',
          'Кропивницький', 'Луганськ', 'Луцьк', 'Львів', 'Миколаїв', 'Одеса', 'Полтава', 'Рівне', 'Севастополь', 'Суми',
          'Тернопіль', 'Ужгород', 'Харків', 'Херсон', 'Хмельницький', 'Черкаси', 'Чернівці', 'Чернігів']
# Adding the rest of cities
with open('main/all_cities.txt', 'r', encoding='utf-8') as all_cities:
    for city in all_cities:
        cities.append(city.strip('\n').strip(' '))

cities_choices = tuple([(city, city) for city in cities])
without_salary_choices = (("True", 'Without salary'),)
emp_choices = (("полная занятость", 'Full-time'), ("неполная занятость", 'Part-time'), ("удаленная работа", 'Remote'))
lang_choices = (("c/c++", 'C/C++'), ("c#", 'C#'), ("java", 'Java'), ("javascript", 'JavaScript'), ("php", 'PHP'),
                ("python", 'Python'), ("ruby", 'Ruby'), ("swift", 'Swift'))
db_choices = (("cassandra", 'Cassandra'), ("db2", 'DB2'), ("mariadb", 'MariaDB'),
              ("microsoft access", 'Microsoft Access'), ("microsoft sql server", 'Microsoft SQL Server'),
              ("mysql", 'MySQL'), ("oracle", 'Oracle'), ("postgresql", 'PostgreSQL'), ("redis", 'Redis'),
              ("sqlite", 'SQLite'))
skills_choices = (("adobe flash", 'Adobe Flash'), ("docker", 'Docker'), ("git", 'Git'), ("html/css", 'HTML/CSS'),
                  ("microsoft excel", 'Microsoft Excel'), (".net", '.NET'), ("nosql", 'NoSQL'), ("qa", 'QA'),
                  ("sql", 'SQL'), ("svn", 'SVN'), ("tcp/ip", 'TCP/IP'), ("1c", '1C'),
                  ("2d", '2D'), ("3d", '3D'))


class RequirementsForm(forms.Form):
    city = forms.ChoiceField(choices=cities_choices, label='', widget=forms.Select(attrs={'class': 'form-control-sm'}),
                             required=False)
    salary = forms.CharField(label='from', widget=forms.TextInput(), required=False)
    without_salary = forms.MultipleChoiceField(choices=without_salary_choices, label='',
                                               widget=forms.CheckboxSelectMultiple(attrs={'checked': 'True'}), required=False)
    emp = forms.MultipleChoiceField(choices=emp_choices, label='', widget=forms.CheckboxSelectMultiple, required=False)
    lang = forms.MultipleChoiceField(choices=lang_choices, label='', widget=forms.CheckboxSelectMultiple,
                                     required=False)
    db = forms.MultipleChoiceField(choices=db_choices, label='', widget=forms.CheckboxSelectMultiple, required=False)
    skills = forms.MultipleChoiceField(choices=skills_choices, label='', widget=forms.CheckboxSelectMultiple,
                                       required=False)


class SearchForm(forms.Form):
    search = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control me-2',
                                                                         'type': 'search', 'placeholder': 'Search',
                                                                         'aria-label': 'Search'}), required=False)

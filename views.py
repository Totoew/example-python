from django.shortcuts import render
from .models import *
import requests
import datetime


def index(request):
    image1 = ImageModel.objects.filter(name='image1').first()
    image2 = ImageModel.objects.filter(name='image2').first()
    return render(request, 'index.html', {'image1': image1, 'image2': image2})


def relevance(request):
    year_salary_image = ImageModel.objects.filter(name='year_salary_image').first()
    year_count_image = ImageModel.objects.filter(name='year_count_image').first()
    year_analytics = YearAnalytics.objects.all()
    return render(request, 'relevance.html', 
                  {'year_analytics': year_analytics,
                   'year_salary_image': year_salary_image, 'year_count_image': year_count_image})


def geography(request):
    area_salary = AreaSalary.objects.all()
    area_part = AreaPart.objects.all()
    area_salary_vac = AreaSalaryVacancy.objects.all()
    area_part_vac = AreaPartVacancy.objects.all()
    area_salary_image = ImageModel.objects.filter(name='area_salary_image').first()
    area_part_image = ImageModel.objects.filter(name='area_part_image').first()
    return render(request, 'geography.html', 
                  {'area_salary': area_salary, 'area_part': area_part, 
                   'area_salary_vac': area_salary_vac, 'area_part_vac': area_part_vac,
                   'area_salary_image': area_salary_image, 'area_part_image': area_part_image})


def skills(request):
    year_skills = YearSkills.objects.exclude(skill1__isnull=True).order_by('-year')
    year_skills_vac = YearSkillsVacancy.objects.exclude(skill1__isnull=True).order_by('-year')
    skills_count_image = ImageModel.objects.filter(name='skills_count_image').first()
    return render(request, 'skills.html', {'year_skills': year_skills, 'year_skills_vac': year_skills_vac,
                                           'skills_count_image': skills_count_image})


def recent_vacancies(request):
    vacancies = get_vacancies()
    for vacancy in vacancies:
        vacancy['key_skills'] = ', '.join(vacancy['key_skills'])

        salary = vacancy['salary']
        if salary == {} or (salary['from'] == None and salary['to'] == None):
            salary['message'] = ' - '
        else:
            if salary['to'] != None and salary['from'] != None:
                salary['message'] = f'{salary["from"]} - {salary["to"]} '
            elif salary['to'] != None:
                salary['message'] = f'до {salary["to"]} '
            else:
                salary['message'] = f'от {salary["from"]} '
                
            if salary['currency'] != None:
                salary['message'] += salary['currency']
            
            if salary['gross'] != None:
                salary['message'] += ' (до вычета налогов)' if salary['gross'] else ' (на руки)'
            
    return render(request, 'recent_vacancies.html', {'vacancies': vacancies})


def get_vacancies():
    url = 'https://api.hh.ru/vacancies'
    profession = 'Frontend программист'
    params = {
        "text": f"NAME:({profession})",
        "order_by": "publication_time",
        "date_from": (datetime.datetime.now() - datetime.timedelta(1)).isoformat(),
        "page": 0,
        "per_page": 10
    }
    response = requests.get(url, params)
    data = response.json()
    vacancies = []
    for vacancy in data['items']:
        id = vacancy['id']
        vacancy_data = requests.get(url + '/' + id).json()
        vacancies.append(
            {
                'name': vacancy_data['name'],
                'description': vacancy_data['description'],
                'key_skills': [skill['name'] for skill in vacancy_data['key_skills']],
                'employer': vacancy_data['employer']['name'],
                'salary': {
                    'currency': vacancy_data['salary']['currency'],
                    'from': vacancy_data['salary']['from'],
                    'to': vacancy_data['salary']['to'],
                    'gross': vacancy_data['salary']['gross']
                } if vacancy['salary'] != None else {},
                'area': vacancy['area']['name'],
                'published_at': vacancy['published_at']
            }
        )
    return vacancies
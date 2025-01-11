import pandas as pd
import sqlite3
import os
from pathlib import Path
import datetime


BASE_DIR = Path(__file__).resolve().parent.parent
database_path = os.path.join(BASE_DIR, 'db.sqlite3')
tags = ['frontend', 'фронтенд', 'вёрстка', 'верстка', 'верста', 'front end', 'angular', 'html', 'css', 'react', 'vue']
profession_name = "Frontend-программист"

# sql boolean condition with search mask by profession tags
tag_mask = " OR ".join([f"name LIKE '%{tag}%'" for tag in tags])


def get_years_salary():
    with sqlite3.connect(database_path) as conn:
        return pd.read_sql('''
                            SELECT substr(published_at, 1, 4) as year, ROUND(AVG(salary), 2) as salary
                            FROM vacancies
                            WHERE salary IS NOT NULL
                            GROUP BY substr(published_at, 1, 4)
                            ORDER BY published_at''', conn)


def get_years_count():
    with sqlite3.connect(database_path) as conn:
        return pd.read_sql('''
                            SELECT substr(published_at, 1, 4) as year, COUNT(*) as count
                            FROM vacancies
                            WHERE salary IS NOT NULL
                            GROUP BY substr(published_at, 1, 4)
                            ORDER BY published_at''', conn)


def get_years_salary_vac():
    with sqlite3.connect(database_path) as conn:
        return pd.read_sql(f'''
                            SELECT substr(published_at, 1, 4) as year, ROUND(AVG(salary), 2) as salary
                            FROM vacancies
                            WHERE salary IS NOT NULL AND ({tag_mask})
                            GROUP BY substr(published_at, 1, 4)
                            ORDER BY published_at''', conn)


def get_years_count_vac():
    with sqlite3.connect(database_path) as conn:
        return pd.read_sql(f'''
                            SELECT substr(published_at, 1, 4) as year, COUNT(*) as count
                            FROM vacancies
                            WHERE salary IS NOT NULL AND ({tag_mask})
                            GROUP BY substr(published_at, 1, 4)
                            ORDER BY published_at''', conn)
    

def get_area_salary():
    with sqlite3.connect(database_path) as conn:
        return pd.read_sql('''
                            SELECT area_name as area, ROUND(AVG(salary), 2) as salary
                            FROM vacancies
                            GROUP BY area_name
                            HAVING COUNT(*) >= (SELECT COUNT(*) FROM vacancies) / 100
                            ORDER BY ROUND(AVG(salary), 2) DESC
                            LIMIT 10''', conn)


def get_area_part():
    with sqlite3.connect(database_path) as conn:
        return pd.read_sql('''
                            SELECT area_name as area, CAST(COUNT(*) AS REAL) / (SELECT COUNT(*) FROM vacancies) as part
                            FROM vacancies
                            GROUP BY area_name
                            HAVING COUNT(*) >= (SELECT COUNT(*) FROM vacancies) / 100
                            ORDER BY CAST(COUNT(*) AS REAL) / (SELECT COUNT(*) FROM vacancies) DESC
                            LIMIT 10''', conn)


def get_area_salary_vac():
    with sqlite3.connect(database_path) as conn:
        return pd.read_sql(f'''
                            SELECT area_name as area, ROUND(AVG(salary), 2) as salary
                            FROM vacancies
                            WHERE {tag_mask}
                            GROUP BY area_name
                            HAVING COUNT(*) >= (SELECT COUNT(*) FROM vacancies WHERE {tag_mask}) / 100
                            ORDER BY ROUND(AVG(salary), 2) DESC
                            LIMIT 10''', conn)


def get_area_part_vac():
    with sqlite3.connect(database_path) as conn:
        return pd.read_sql(f'''
                            SELECT area_name as area, CAST(COUNT(*) AS REAL) / (SELECT COUNT(*) FROM vacancies WHERE {tag_mask}) as part
                            FROM vacancies
                            WHERE {tag_mask}
                            GROUP BY area_name
                            HAVING COUNT(*) >= (SELECT COUNT(*) FROM vacancies WHERE {tag_mask}) / 100
                            ORDER BY CAST(COUNT(*) AS REAL) / (SELECT COUNT(*) FROM vacancies WHERE {tag_mask}) DESC
                            LIMIT 10''', conn)


def get_years_skills():
    with sqlite3.connect(database_path) as conn:
        years = pd.read_sql('''
                            SELECT DISTINCT substr(published_at, 1, 4) as year
                            FROM vacancies
                            ''', conn)['year']
        
        result = pd.DataFrame(index=years, columns=[i for i in range(20)])

        for year in years:
            series = pd.read_sql(f'''
                            SELECT key_skills as skill
                            FROM vacancies JOIN skills
                            ON vacancies.vacancy_id = skills.vacancy_id
                            WHERE substr(published_at, 1, 4) = '{year}'
                            GROUP BY key_skills
                            ORDER BY COUNT(*) DESC
                            LIMIT 20''', conn)['skill']

            result.loc[year] = series
        result.columns = [f'skill{i}' for i in range(1, 21)]
        return result.reset_index()
    

def get_years_skills_vac():
    with sqlite3.connect(database_path) as conn:
        years = pd.read_sql('''
                            SELECT DISTINCT substr(published_at, 1, 4) as year
                            FROM vacancies
                            ''', conn)['year']
        
        result = pd.DataFrame(index=years, columns=[i for i in range(20)])

        for year in years:
            series = pd.read_sql(f'''
                            SELECT key_skills as skill
                            FROM vacancies JOIN skills
                            ON vacancies.vacancy_id = skills.vacancy_id
                            WHERE substr(published_at, 1, 4) = '{year}' AND ({tag_mask})
                            GROUP BY key_skills
                            ORDER BY COUNT(*) DESC
                            LIMIT 20''', conn)['skill']

            result.loc[year] = series
        result.columns = [f'skill{i}' for i in range(1, 21)]
        return result.reset_index()


def get_skills_count():
    with sqlite3.connect(database_path) as conn:
        year = datetime.date.today().year - 1
        return pd.read_sql(f'''
                        SELECT key_skills as skill, COUNT(*) as count
                        FROM vacancies JOIN skills
                        ON vacancies.vacancy_id = skills.vacancy_id
                        WHERE substr(published_at, 1, 4) = '{year}'
                        GROUP BY key_skills
                        ORDER BY COUNT(*) DESC
                        LIMIT 20''', conn)


def get_skills_count_vac():
    with sqlite3.connect(database_path) as conn:
        year = datetime.date.today().year - 1
        return pd.read_sql(f'''
                        SELECT key_skills as skill, COUNT(*) as count
                        FROM vacancies JOIN skills
                        ON vacancies.vacancy_id = skills.vacancy_id
                        WHERE substr(published_at, 1, 4) = '{year}' AND ({tag_mask})
                        GROUP BY key_skills
                        ORDER BY COUNT(*) DESC
                        LIMIT 20''', conn)
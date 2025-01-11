import analytics
import plots
import pandas as pd
import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
root = os.path.join(BASE_DIR, 'data')


def export_csv(df: pd.DataFrame, table_name: str):
    df.to_csv(os.path.join(root, table_name + '.csv'), index=False)


if __name__=="__main__":
    os.makedirs(root, exist_ok=True)
    years_salary = analytics.get_years_salary()
    years_salary_vac = analytics.get_years_salary_vac()
    years_count = analytics.get_years_count()
    years_count_vac = analytics.get_years_count_vac()
    area_salary = analytics.get_area_salary()
    area_part = analytics.get_area_part()
    area_salary_vac = analytics.get_area_salary_vac()
    area_part_vac = analytics.get_area_part_vac()
    years_skills = analytics.get_years_skills()
    years_skills_vac = analytics.get_years_skills_vac()
    skills_count = analytics.get_skills_count()
    skills_count_vac = analytics.get_skills_count_vac()

    year_analytics = years_salary
    year_analytics['count'] = years_count['count']
    year_analytics['salary_vac'] = years_salary_vac['salary']
    year_analytics['count_vac'] = years_count_vac['count']

    plots.export_years_salary(years_salary, years_salary_vac)
    plots.export_years_count(years_count, years_count_vac)
    plots.export_area_salary(area_salary, area_salary_vac)
    plots.export_area_part(area_part, area_part_vac)
    plots.export_skills_count(skills_count, skills_count_vac)

    export_csv(year_analytics, 'year_analytics')
    export_csv(area_salary, 'area_salary')
    export_csv(area_part, 'area_part')
    export_csv(area_salary_vac, 'area_salary_vacancy')
    export_csv(area_part_vac, 'area_part_vacancy')
    export_csv(years_skills, 'year_skills')
    export_csv(years_skills_vac, 'year_skills_vacancy')
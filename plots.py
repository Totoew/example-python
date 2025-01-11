import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
import os


BASE_DIR = Path(__file__).resolve().parent.parent
root = os.path.join(BASE_DIR, 'data')
profession = 'Frontend-программист'


def export_years_salary(df: pd.DataFrame, df_vac: pd.DataFrame):
    bar_width = 0.4
    plt.subplots(figsize=(5, 5), dpi=100)
    plt.title('Уровень зарплат по годам')
    plt.bar(list(map(lambda x: int(x), df['year'])), df['salary'], width=bar_width, label='средняя з/п')
    plt.bar(list(map(lambda x: int(x) + bar_width, df_vac['year'])), df_vac['salary'], width=bar_width, label=f'з/п {profession}')
    plt.legend(fontsize=8)
    plt.tick_params(axis='both', labelsize=8)
    plt.xticks(
        list(map(lambda x: int(x) + bar_width / 2, df['year'])),
        df['year'], rotation=90, ha='center'
    )
    plt.grid(True, axis='y')

    plt.savefig(os.path.join(root, 'years_salary.png'))
    # plt.show()


def export_years_count(df: pd.DataFrame, df_vac: pd.DataFrame):
    bar_width = 0.4
    fig, sub = plt.subplots(1, 2, figsize=(15, 5), dpi=100)
    fig.suptitle('Количество вакансий по годам')
    sub[0].bar(list(map(lambda x: int(x), df['year'])), df['count'], width=bar_width, label='кол-во вакансий')
    sub[0].legend(fontsize=8)
    sub[0].set_xticks(list(map(lambda x: int(x), df['year'])))
    sub[0].set_xticklabels(df['year'], rotation=90, ha='center')
    sub[0].tick_params(axis='both', labelsize=8)
    sub[0].yaxis.grid(True)

    sub[1].bar(list(map(lambda x: int(x), df_vac['year'])), df_vac['count'], width=bar_width, label=f'кол-во вакансий\n{profession}')
    sub[1].legend(fontsize=8)
    sub[1].set_xticks(list(map(lambda x: int(x), df_vac['year'])))
    sub[1].set_xticklabels(df_vac['year'], rotation=90, ha='center')
    sub[1].tick_params(axis='both', labelsize=8)
    sub[1].yaxis.grid(True)

    plt.savefig(os.path.join(root, 'years_count.png'))
    # plt.show()


def export_area_salary(df: pd.DataFrame, df_vac: pd.DataFrame):
    fig, sub = plt.subplots(1, 2, figsize=(15, 5), dpi=100)
    fig.suptitle('Уровень зарплат по городам')
    sub[0].invert_yaxis()
    sub[0].barh(df['area'], df['salary'], align='center', label='средняя з/п')
    sub[0].legend(fontsize=8)
    sub[0].set_yticklabels(df['area'].str.replace('-', '-\n').str.replace(' ', '\n'), ha="right", va="center")
    sub[0].tick_params(axis='y', labelsize=8)
    sub[0].tick_params(axis='x', labelsize=8)
    sub[0].xaxis.grid(True)

    sub[1].invert_yaxis()
    sub[1].barh(df_vac['area'], df_vac['salary'], align='center', label=f'средняя з/п\n{profession}')
    sub[1].legend(fontsize=8)
    sub[1].set_yticklabels(df_vac['area'].str.replace('-', '-\n').str.replace(' ', '\n'), ha="right", va="center")
    sub[1].tick_params(axis='y', labelsize=8)
    sub[1].tick_params(axis='x', labelsize=8)
    sub[1].xaxis.grid(True)

    plt.savefig(os.path.join(root, 'area_salary.png'))
    # plt.show()


def export_area_part(df: pd.DataFrame, df_vac: pd.DataFrame):
    fig, sub = plt.subplots(1, 2, figsize=(15, 5), dpi=100)
    part = df['part']
    part.index = df['area']
    part["Другие"] = 1 - part.sum()
    sub[0].set_title('Доля вакансий по городам')
    sub[0].pie(part, labels=part.index, startangle=90, textprops={'fontsize': 6})
    sub[0].axis('equal')
    sub[0].tick_params(axis='both', labelsize=6)

    part = df_vac['part']
    part.index = df_vac['area']
    part["Другие"] = 1 - part.sum()
    sub[1].set_title(f'Доля вакансий по городам\n{profession}')
    sub[1].pie(part, labels=part.index, startangle=90, textprops={'fontsize': 6})
    sub[1].axis('equal')
    sub[1].tick_params(axis='both', labelsize=6)

    plt.savefig(os.path.join(root, 'area_part.png'))
    # plt.show()


def export_skills_count(df: pd.DataFrame, df_vac: pd.DataFrame):
    bar_width = 0.4
    fig, sub = plt.subplots(1, 2, figsize=(15, 5), dpi=100)
    fig.suptitle('Колличество вакансий с необходимыми навыками')
    sub[0].bar(df['skill'], df['count'], width=bar_width, label='кол-во вакансий')
    sub[0].legend(fontsize=8)
    sub[0].set_xticklabels(df['skill'], rotation=90, ha='center')
    sub[0].tick_params(axis='both', labelsize=8)
    sub[0].yaxis.grid(True)

    sub[1].bar(df_vac['skill'], df_vac['count'], width=bar_width, label=f'кол-во вакансий\n{profession}')
    sub[1].legend(fontsize=8)
    sub[1].set_xticklabels(df_vac['skill'], rotation=90, ha='center')
    sub[1].tick_params(axis='both', labelsize=8)
    sub[1].yaxis.grid(True)

    plt.savefig(os.path.join(root, 'skills_count.png'))
    # plt.show()
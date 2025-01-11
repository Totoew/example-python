import pandas as pd
import sqlite3
import currencies


def convert(vacancy: pd.Series, currency_rate: pd.DataFrame) -> pd.Series:
    """
    Convert salary of given vacancy series

    """
    salary = vacancy['salary']
    currency = vacancy['salary_currency']
    date = vacancy['published_at'][:7]
    if pd.isna(salary) or pd.isna(currency) or currency == 'RUR':
        return vacancy
    rate = currency_rate.at[date, currency]
    vacancy['salary'] = int(vacancy['salary'] * rate) if pd.notna(rate) else None
    if vacancy.name % 1000 == 0:
        print(vacancy)
    return vacancy


vacancies_path = 'scripts/vacancies_2024.csv'
chunksize = 10000


def load_vacancies(currency_rate: pd.DataFrame) -> None:
    """
    Read csv file by chunks and load records to database with converted currencies

    """
    chunks = pd.read_csv(vacancies_path, chunksize=chunksize)
    
    with sqlite3.connect('db.sqlite3') as conn:
        for chunk in chunks:
            chunk.assign(
                salary_from=chunk['salary_from'].fillna(chunk['salary_to']),
                salary_to=chunk['salary_to'].fillna(chunk['salary_from'])
            ).assign(
                salary=(chunk['salary_from'] + chunk['salary_to']) / 2
            ).apply(
                lambda row: convert(row, currency_rate), axis=1
            )[['name', 'salary', 'area_name', 'published_at']].to_sql('vacancies', conn, if_exists='append', index_label='vacancy_id')

            chunk['key_skills'].dropna().apply(
                lambda val: val.split('\n') if pd.notna(val) else pd.NA
            ).explode().to_sql('skills', conn, if_exists='append', index_label='vacancy_id')


if __name__=="__main__":
    currency_rate = currencies.get_currencies()
    load_vacancies(currency_rate)

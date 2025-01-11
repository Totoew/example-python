import pandas as pd
from datetime import datetime
from dateutil.rrule import rrule, MONTHLY
import requests
import io


url = f"http://www.cbr.ru/scripts/XML_daily.asp"

index = ['date', 'BYR' , 'USD', 'EUR', 'KZT', 'UAH', 'AZN', 'KGS', 'UZS', 'GEL']

start = datetime(2003, 1, 1)

def get_currencies() -> pd.DataFrame:
    """
    Load currency rate from cbr.ru

    :return: dataframe of rates by months
    """
    answer = pd.DataFrame()

    end = datetime.now()
    
    for d in rrule(MONTHLY, dtstart=start, until=end):
        response = requests.get(f'{url}?date_req={d.strftime("%d/%m/%Y")}')
        
        curr = pd.read_xml(io.StringIO(response.text))
        

        curr.index = curr['CharCode']
        curr['Value'] = curr['VunitRate'].str.replace(',', '.').astype(float)
        row = pd.concat([
            pd.Series([d.strftime('%Y-%m')], index=['date']), 
            curr['Value']])
        answer = pd.concat([answer, row.reindex(index).to_frame().T], ignore_index=True)

    answer.index = answer['date']
    answer = answer.drop('date', axis=1)
    return answer
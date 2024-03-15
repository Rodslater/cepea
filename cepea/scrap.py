import requests
import os
import pandas as pd

from tqdm import tqdm
from pyexcel_xls import get_data
from datetime import datetime

def download_file(url, file_name):
    headers = {"User-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36"}
    response = requests.get(url, stream=True, headers=headers)
    with open(file_name, "wb") as handle:
        for data in tqdm(response.iter_content()):
            handle.write(data)

def get_cepea_data(commodity, url):
    file_path = os.path.join('cepea', f"{commodity}.xls")
    download_file(url, file_path)
    data = get_data(file_path)
    df = pd.DataFrame(data[0][3:], columns=data[0][2])
    df["Data"] = pd.to_datetime(df["Data"], format='%d/%m/%Y')
    df.set_index("Data", inplace=True)
    df.to_csv(f'cepea/{commodity}.csv')

commodities = [
    {'name': 'etanol_hidratado', 'url': 'https://www.cepea.esalq.usp.br/br/indicador/series/etanol.aspx?id=103'},
    {'name': 'boi_gordo', 'url': 'https://www.cepea.esalq.usp.br/br/indicador/series/boi-gordo.aspx?id=2'},
    {'name': 'milho', 'url': 'https://www.cepea.esalq.usp.br/br/indicador/series/milho.aspx?id=77'}
]

for commodity in commodities:
    get_cepea_data(commodity['name'], commodity['url'])


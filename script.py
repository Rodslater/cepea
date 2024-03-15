import requests
import time
import csv
import datetime
import os
from tqdm import tqdm
import pyexcel_xls
import OleFileIO_PL
import datetime as dt
import pandas as pd

def remove_old_files():
    file_list = os.listdir(r"cepea")
    for file_name in file_list:
        if not file_name.endswith('.xls'):
            continue
        os.remove(os.path.join('cepea', file_name))
 
def download_file(url, file_name):
    headers = {"User-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36"}
    response = requests.get(url, stream=True, headers=headers)
    with open(file_name, "wb") as handle:
        for data in tqdm(response.iter_content()):
            handle.write(data)
    handle.close()


dados = [
    {'base_name': 'etanol_hidratado', 'url': 'https://www.cepea.esalq.usp.br/br/indicador/series/' + 'etanol.aspx?id=103'},
    {'base_name': 'etanol_anidro', 'url': 'https://www.cepea.esalq.usp.br/br/indicador/series/' + 'etanol.aspx?id=104'},
    {'base_name': 'frango_congelado', 'url': 'https://www.cepea.esalq.usp.br/br/indicador/series/' + 'frango.aspx?id=181'},
    {'base_name': 'frango_resfriado', 'url': 'https://www.cepea.esalq.usp.br/br/indicador/series/' + 'frango.aspx?id=130'},
    {'base_name': 'milho', 'url': 'https://www.cepea.esalq.usp.br/br/indicador/series/' + 'milho.aspx?id=77'},
    {'base_name': 'soja_parana', 'url': 'https://www.cepea.esalq.usp.br/br/indicador/series/' + 'soja.aspx?id=12'},
    {'base_name': 'trigo_parana', 'url': 'https://www.cepea.esalq.usp.br/br/indicador/series/' + 'trigo.aspx?id=178'}
]


# faz o download do excel no site do CEPEA
remove_old_files()

for dado in dados:
    name_file = dado['base_name'] + '_' + time.strftime("%d.%m.%Y") + '.xls'
    path_file = os.path.join('cepea', name_file)
    download_file(dado['url'], path_file)
    print(path_file)
    

#função que retorna um dataframe dos dados do CEPEA
def dados_cepea(commoditie):
    name_file = "cepea/" + commoditie + '_' + time.strftime("%d.%m.%Y") + '.xls'
    with open(name_file,'rb') as file:
        ole = OleFileIO_PL.OleFileIO(file)
        if ole.exists('Workbook'):
            d = ole.openstream('Workbook')
            df = pd.read_excel(d,engine='xlrd', skiprows=3)
            df["Data"] = pd.to_datetime(df["Data"], format='%d/%m/%Y') 
            df = df.set_index("Data")
            return df
        
#Chamando a função para cada uma das commodities
etanol_hidratado = dados_cepea('etanol_hidratado')
etanol_anidro = dados_cepea('etanol_anidro')
frango_congelado = dados_cepea('frango_congelado')
frango_resfriado = dados_cepea('frango_resfriado')
milho = dados_cepea('milho')
soja_parana = dados_cepea('soja_parana')
trigo_parana = dados_cepea('trigo_parana')

import requests
import csv
import os
from tqdm import tqdm
import pyexcel_xls
import OleFileIO_PL
import pandas as pd
 
def download_file(url, file_name):
    headers = {"User-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36"}
    response = requests.get(url, stream=True, headers=headers)
    with open(file_name, "wb") as handle:
        for data in tqdm(response.iter_content()):
            handle.write(data)
    handle.close()

dados = [
    {'base_name': 'etanol_hidratado', 'url': 'https://www.cepea.esalq.usp.br/br/indicador/series/' + 'etanol.aspx?id=103'},
    {'base_name': 'boi_gordo', 'url': 'https://www.cepea.esalq.usp.br/br/indicador/series/' + 'boi-gordo.aspx?id=2'}, 
    {'base_name': 'milho', 'url': 'https://www.cepea.esalq.usp.br/br/indicador/series/' + 'milho.aspx?id=77'}
]

# faz o download do excel no site do CEPEA
for dado in dados:
    name_file = dado['base_name'] + '.xls'
    path_file = os.path.join('cepea', name_file)
    download_file(dado['url'], path_file)
    print(path_file)
    

#função que retorna um dataframe dos dados do CEPEA
def dados_cepea(commoditie):
    name_file = "cepea/" + commoditie + '.xls'
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
boi_gordo = dados_cepea('boi_gordo')
milho = dados_cepea('milho')

etanol_hidratado.to_csv('cepea/etanol_hidratado.csv')
milho.to_csv('cepea/milho.csv')
boi_gordo.to_csv('cepea/boi_gordo.csv')

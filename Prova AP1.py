# Programação para Análise de Dados - AP1
# Alexandre de Sousa Campos Menezes - 202303035454
# Date: 16/04/2026

#----------------------------------------------------

# Bibliotecas
import pandas as pd
import requests

#----------------------------------------------------

# O dataset LOGCP - base_tickets_manutencao_historico.xlsx contém o histórico de incidentes da empresa.
# Através da importantação dos dados através da biblioteca pandas, responda as perguntas abaixo.

df = pd.read_excel("LOGCP_-_base_tickets_manutencao_historico.xlsx")

# 1 - (1,0) Quantos tickets foram (utilize a coluna "des_status"):
#    - Abertos?
#    - Concluídos?
#    - Cancelados?

print(df.head())
print(df.columns.tolist())

filtro1 = df["des_status"] == "open"
df.loc[filtro1, :]

filtro2 = df["des_status"] == "solved"
df.loc[filtro2, :]

filtro3 = df["des_status"] == "pending"
df.loc[filtro3, :]

# 2 - (1,0) Qual a taxa de conclusão dos tickets em relação ao total?

total_tickets = df.shape[0]
concluidos = df[df["des_status"] == "solved"].shape[0]

taxa_conclusao = concluidos / total_tickets
print(f"Taxa de conclusão: {taxa:.2%}")

# 3 - (1,0) Qual categoria tem mais tickets(utilize a coluna "des_categoria")?
categoria_tickets = df["des_categoria"]
print(categoria_tickets)

# 4 - (1,0) Qual categoria tem maior numero de de cancelamento?

df_cancelados = df[df["des_status"] == "pending"]
print(df_cancelados["des_categoria"].value_counts().idxmax())

# 5 - (1,0) Quanto rendeu a VALE3 nos ultimos 5 anos entre 2020 e 2025?
# base_url = "https://laboratoriodefinancas.com/api/v2"
# token = "SEU_JWT"
# params = {"ticker": "VALE3", "data_ini": "2001-01-01", "data_fim": "2026-12-31"}
# response = requests.get(
#     f"{base_url}/preco/corrigido",
#     headers={"Authorization": f"Bearer {token}"},
#     params=params,
# )

base_url = "https://laboratoriodefinancas.com/api/v2"
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzc4ODUwNzA2LCJpYXQiOjE3NzYyNTg3MDYsImp0aSI6IjFiYmU5YmU4MTg0ZjQ2MDBhZDM5MjMwYmYwY2QwOWJlIiwidXNlcl9pZCI6IjEwOCJ9.SkNNEugjRw905AZ_Dsn6UA_giH_0VLW0huPKwzPTkJ8"

params_vale = {
    "ticker": "VALE3",
    "data_ini": "2020-01-01",
    "data_fim": "2025-12-31",
}
response_vale = requests.get(
    f"{base_url}/preco/corrigido",
    headers={"Authorization": f"Bearer {token}"},
    params=params_vale,
)
df_vale = pd.DataFrame(response_vale.json())
df_vale["fechamento"] = pd.to_numeric(df_vale["fechamento"])
df_vale["data"] = pd.to_datetime(df_vale["data"])
df_vale = df_vale.sort_values("data")

preco_inicial_vale = df_vale.iloc[0]["fechamento"]
preco_final_vale = df_vale.iloc[-1]["fechamento"]
retorno_vale = (preco_final_vale / preco_inicial_vale) - 1
print(f"Rendimento VALE3 (2020-2025): {retorno_vale:.2%}")

# 6 - (1,0) A BrasilAPI disponibiliza informações da tabela FIPE, incluindo marcas, modelos e preços de veículos.
# Acesse o endpoint de marcas da FIPE para o tipo de veículo carros.
# import requests
# import pandas as pd
# tipoVeiculo = "carros"
# api = f"https://brasilapi.com.br/api/fipe/marcas/v1/{tipoVeiculo}"
# Transforme em DataFrame e acha o codigo BYD através da coluna "nome"
# Use esse código para acessar o endpoint de modelos da marca BYD.
# codigoMarca=""
# api = f"https://brasilapi.com.br/api/fipe/veiculos/v1/{tipoVeiculo}/{codigoMarca}"
# Construa um DataFrame com os modelos disponíveis.
# Responda: quantos modelos de veículos BYD estão cadastrados na FIPE?

tipoVeiculo = "carros"
api = f"https://brasilapi.com.br/api/fipe/marcas/v1/{tipoVeiculo}"

df_marcas = pd.DataFrame(requests.get(api).json())

codigoMarca = df_marcas[df_marcas["nome"].str.contains("BYD", case=False)]["valor"].values[0]
print(f"Código BYD: {codigoMarca}")

api = f"https://brasilapi.com.br/api/fipe/veiculos/v1/{tipoVeiculo}/{codigoMarca}"
df_byd = pd.DataFrame(requests.get(api).json())

print(f"Modelos BYD cadastrados: {df_byd.shape[0]}")

codigoMarca = "238"
api = f"https://brasilapi.com.br/api/fipe/veiculos/v1/{tipoVeiculo}/{codigoMarca}"

df_byd = pd.DataFrame(requests.get(api).json())
print(f"Modelos BYD cadastrados: {df_byd.shape[0]}")

# 7 - (1,0) O Banco Mundial disponibiliza uma API pública com diversos indicadores econômicos. 
# O código do indicador NY.GDP.PCAP.CD corresponde ao PIB per capita (em dólares correntes).
# Usando Python e a biblioteca requests para acessar a API e pandas para manipulação dos dados:
# Acesse o indicador "NY.GDP.PCAP.CD" e o pais "BRA".
# url = f"https://api.worldbank.org/v2/country/{pais}/indicator/{indicador}?format=json"
# Construa um DataFrame atraves do segundo elemento da lista do retorno
# Selecione apenas as colunas anos (date) e os valores de PIB per capita (value).
# Identifique em qual ano o Brasil apresentou o menor PIB per capita e mostre o respectivo valor.

pais = "BRA"
indicador = "NY.GDP.PCAP.CD"
url = f"https://api.worldbank.org/v2/country/{pais}/indicator/{indicador}?format=json"

response_wb = requests.get(url)
df_pib = pd.DataFrame(response_wb.json()[1])

df_pib = df_pib[["date", "value"]].dropna()

menor_pib = df_pib[df_pib["value"] == df_pib["value"].min()]
print(menor_pib)

# 8 - (1,0) - Faça um ranking das 30 melhores empresas baseado nos indicadores Return on Equity (roe) e Dividend Yield (dividend_yield) no dia 2024-04-01.
# Faça uma média entre o ranking das empresas com maior ROE e o ranking das empresas com maior dividend_yield
# base_url = "https://laboratoriodefinancas.com/api/v2"
# token = "SEU_JWT"
# response = requests.get(
#     f"{base_url}/bolsa/planilhao",
#     headers={"Authorization": f"Bearer {token}"},
#     params={"data_base": "2026-04-01"},
# )

base_url = "https://laboratoriodefinancas.com/api/v2"
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzc4ODUwNzA2LCJpYXQiOjE3NzYyNTg3MDYsImp0aSI6IjFiYmU5YmU4MTg0ZjQ2MDBhZDM5MjMwYmYwY2QwOWJlIiwidXNlcl9pZCI6IjEwOCJ9.SkNNEugjRw905AZ_Dsn6UA_giH_0VLW0huPKwzPTkJ8"
response = requests.get(
    f"{base_url}/bolsa/planilhao",
    headers={"Authorization": f"Bearer {token}"},
    params={"data_base": "2024-04-01"},
)



# 9 - (1,0) Quantos setores ("setor") tem essa carteira formada por 30 ações?


# 10 - (1,0) 11 - Você tem acesso à API do Laboratório de Finanças, que fornece dados do Planilhão em formato JSON. 
# Selecione a empresa do setor de "varejo" que apresenta o maior endividamento na data base 2024-04-01.
# Exiba APENAS AS COLUNAS "ticker", "setor", "preco", "endividamento"
# base_url = "https://laboratoriodefinancas.com/api/v2"
# token = "SEU_JWT"
# response = requests.get(
#     f"{base_url}/bolsa/planilhao",
#     headers={"Authorization": f"Bearer {token}"},
#     params={"data_base": "2026-04-01"},
# )

base_url = "https://laboratoriodefinancas.com/api/v2"
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzc4ODUwNzA2LCJpYXQiOjE3NzYyNTg3MDYsImp0aSI6IjFiYmU5YmU4MTg0ZjQ2MDBhZDM5MjMwYmYwY2QwOWJlIiwidXNlcl9pZCI6IjEwOCJ9.SkNNEugjRw905AZ_Dsn6UA_giH_0VLW0huPKwzPTkJ8"
response = requests.get(
    f"{base_url}/bolsa/planilhao",
    headers={"Authorization": f"Bearer {token}"},
    params={"data_base": "2024-04-01"},
)

data_planilhao = response.json()
df_planilhao = pd.DataFrame(data_planilhao)

print(df_planilhao.head())
print(df_planilhao.columns.tolist())

print(df_planilhao[["ticker", "setor", "preco", "endividamento"]])
filtro1_setor = df_planilhao[df_planilhao["setor"] == "varejo"]
print(filtro1_setor)
maior_endividamento = filtro1_setor[filtro1_setor["preco"] == filtro1_setor["preco"].max()]
print(maior_endividamento[["ticker", "setor", "preco", "endividamento"]])


# 11 - (1,0) O IPEA disponibiliza uma API pública com diversas séries econômicas.
# Para localizar uma série de interesse, é necessário acessar primeiro o endpoint de metadados.
# Acesse o endpoint de metadados:
# "http://www.ipeadata.gov.br/api/odata4/Metadados"
# Transforme o retorno em um DataFrame.
# Filtre para encontrar as séries do IBGE relacionadas à taxa de desemprego no Brasil.
# Dica:
# - Utilize a coluna FNTSIGLA para encontrar as séries do "IBGE";
# - Utilize a coluna SERNOME para encontrar as séries relacionadas a "Taxa de desemprego - cor negra"

url = "http://www.ipeadata.gov.br/api/odata4/Metadados"
response = requests.get(url)
data = response.json()
df_ipea = pd.DataFrame(data["value"])
df_ipea.head()

print(df_ipea.columns.tolist())

filtro1_ibge = df_ipea["FNTSIGLA"].str.contains("IBGE", case=False, na=False)
filtro2_tx_desemprego = df_ipea["SERNOME"].str.contains("Taxa de desemprego - cor negra", case=False, na=False)
df_ibge = df_ipea[filtro1_ibge & filtro2_tx_desemprego]
print(df_ibge[["FNTSIGLA", "SERNOME"]])

# 12 - (1,0) Descubra qual é o código da série correspondente (coluna: SERCODIGO).
# CODIGO_ENCONTRADO = ''
# Usando o código encontrado, acesse a API de valores:
# f"http://ipeadata.gov.br/api/odata4/ValoresSerie(SERCODIGO='{CODIGO_ENCONTRADO}')"
# Construa um DataFrame a partir da chave 'value' do retorno da API.
# Selecione apenas as colunas de data (VALDATA) e valor (VALVALOR).
# Exiba a Data e o Valor em que a taxa de desemprego atingiu o maior valor da série.

print(df_ibge["SERCODIGO"].values)
CODIGO_ENCONTRADO = 'PNADCT_TXDSCUPUF_NEG'
url_valores = f"http://ipeadata.gov.br/api/odata4/ValoresSerie(SERCODIGO='{CODIGO_ENCONTRADO}')"
response_valores = requests.get(url_valores)
data_valores = response_valores.json()

df_valores = pd.DataFrame(data_valores["value"])
df_valores = df_valores[["VALDATA", "VALVALOR"]]
print(df_valores[df_valores["VALVALOR"] == df_valores["VALVALOR"].max()])
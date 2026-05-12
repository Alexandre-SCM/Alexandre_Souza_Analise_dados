import seaborn as sns
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt

df  = sns.load_dataset("tips")
df.info()
df.head()

# Regressão linear simples
# x = total_bill
# y = tip
X = df['total_bill']
y = df['tip']

#adiciona o intercepto 
x = sm.add_constant(X)
modelo = sm.OLS(y, x).fit()
print(modelo.summary())

# plot
sns.lmplot(data=df, x="total_bill", y="tip")
modelo.params
modelo.pvalues
modelo.df_model
modelo.rsquared

# Regressão linear multipla
# X = total_bill, size
# y = tip

X = df[['total_bill', 'size']]
y = df['tip']

x = sm.add_constant(X)
modelo = sm.OLS(y, x).fit()
print(modelo.summary())

# Residuo de regressão
df['tip'] - modelo.predict()

# Pegando uma Serie de Dados - Ibov
from statsmodels.tsa.ar_model import AutoReg
import requests
import pandas as pd

base_url = "https://laboratoriodefinancas.com/api/v2"
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzc4ODUwNzA2LCJpYXQiOjE3NzYyNTg3MDYsImp0aSI6IjFiYmU5YmU4MTg0ZjQ2MDBhZDM5MjMwYmYwY2QwOWJlIiwidXNlcl9pZCI6IjEwOCJ9.SkNNEugjRw905AZ_Dsn6UA_giH_0VLW0huPKwzPTkJ8"
params = {"ticker": "ibov", "data_ini": "2000-01-01", "data_fim": "2025-12-31"}
resp = requests.get(
    f"{base_url}/preco/diversos",
    headers={"Authorization": f"Bearer {token}"},
    params=params,
)
dados = resp.json()
ibov = pd.DataFrame(dados)

x = ibov['fechamento'].astype("float")
# Modelo AR - autorregressivo para series temporais
modelo = AutoReg(x, lags=1).fit()
print(modelo.summary())
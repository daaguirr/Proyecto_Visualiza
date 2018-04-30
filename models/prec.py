import os

import matplotlib.pyplot as plt
import pandas as pd

directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_path = os.path.join(directory, "data")
file_path = os.path.join(data_path, "cr2_prAmon_2018_ghcn/cr2_prAmon_2018_ghcn.txt")

raw = pd.read_table(file_path, sep=",", index_col=0, na_values=[-9999, "-"],
                    low_memory=False)
table = raw.transpose()
groups = table.columns.to_series().groupby(table.dtypes).groups

table[table.columns.values[14:]] = table[table.columns.values[14:]].apply(pd.to_numeric)
table[['altura', 'latitud', 'longitud', 'codigo_cuenca', 'codigo_sub_cuenca', 'cantidad_observaciones']] = table[
    ['altura', 'latitud', 'longitud', 'codigo_cuenca', 'codigo_sub_cuenca', 'cantidad_observaciones']].apply(
    pd.to_numeric)
table[['inicio_observaciones', 'fin_observaciones', 'inicio_automatica']] = \
    table[['inicio_observaciones', 'fin_observaciones', 'inicio_automatica']].apply(pd.to_datetime)

props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)

c = table['1995-07']
ax = c.plot.hist(use_index=True)
plt.text(0.75, 0.95, f"nulls = {c.isnull().sum()}", transform=ax.transAxes, fontsize=14,
         verticalalignment='top')
plt.show()

k = table[table.columns.values[14:]].isnull().sum()
k.index.name = 'meses'
k.index = k.index.map(lambda x: pd.Period(x))

dates = k.index.values
ts = pd.DataFrame({'date': dates,
                   'nulls': k.values}).set_index('date')
ax1 = ts.plot()
plt.text(0.5, 0.9, f"total de estaciones= {k.size}", transform=ax.transAxes, fontsize=14,
         verticalalignment='top')
ax1.set_ylabel("cantidad de estaciones con datos nulls")

plt.show()


def region(lat, lng):
    if lat > -27.6307621:
        return 0  # "Norte Grande"
    if lat > -32.759362:
        return 1  # "Norte Chico"
    if lat > -38.0613847:
        return 2  # "Central"
    if lat > -43.7890687:
        return 3  # "Sur"
    if lat > -56:
        return 4  # "Austral"
    else:
        return 5  # "Antartica"


def str_region(n):
    if n == 0:
        return "Norte Grande"
    if n == 1:
        return "Norte Chico"
    if n == 2:
        return "Central"
    if n == 3:
        return "Sur"
    if n == 4:
        return "Austral"
    else:
        return "Antartica"


zona = table[['latitud', 'longitud']].apply(lambda x: region(x['latitud'], x['longitud']), axis=1)
table['zona'] = zona

gb = table[table.columns.values[14:]].groupby(['zona'], axis=0)
final = gb.apply(lambda x: x[14:].mean())
final.index = final['zona']
final = final.drop(['zona'], axis=1)
final.columns = final.columns.map(lambda x: pd.Period(x))

for i, row in final.iterrows():
    axn = row.plot()
    plt.title(str_region(i))
    plt.xlabel("tiempo")
    plt.ylabel("promedio de precipitaciones (mm)")
    plt.show()

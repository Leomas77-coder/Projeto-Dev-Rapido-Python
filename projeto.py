import pandas as pd
import tkinter as tk

# Lendo o arquivo CSV do caminho do upload
df = pd.read_csv("Tuberculosis_Trends.csv")

# Remove alguns países específicos
df = df[~df['Country'].isin(['Indonesia', 'Bangladesh', 'Nigeria', 'Pakistan', 'India'])]

# Mapeando os países para continentes
continent_map = {
    'Brazil': 'South America',
    'China': 'Asia',
    'South Africa': 'Africa',
    'USA': 'North America',
    'Russia': 'Europe'
}
df['Region'] = df['Country'].map(continent_map)

# Parte para exibir tudo (usar apenas para testes, depois remover)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

# Exibir dataframe e colunas
print(df)
print(df.columns)

# Encontrar o ano mais recente
ano_mais_recente = df['Year'].max()

# Filtrar dados do ano mais recente
df_recente = df[df['Year'] == ano_mais_recente]

print(f"Ano mais recente: {ano_mais_recente}")
print(df_recente.head())


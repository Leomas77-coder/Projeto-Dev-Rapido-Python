import pandas as pd
import plotly.express as px
import webview
import tempfile
import os
import subprocess

# === Carregar e preparar os dados ===
df = pd.read_csv("Tuberculosis_Trends.csv")

# Remove países fora do foco
df = df[~df['Country'].isin(['Indonesia', 'Bangladesh', 'Nigeria', 'Pakistan', 'India'])]

# Mapeia os países para regiões
continent_map = {
    'Brazil': 'South America',
    'China': 'Asia',
    'South Africa': 'Africa',
    'USA': 'North America',
    'Russia': 'Europe'
}
df['Region'] = df['Country'].map(continent_map)

# === Traduções dos nomes dos países e colunas ===
nome_paises_pt = {
    "Brazil": "Brasil",
    "China": "China",
    "South Africa": "África do Sul",
    "USA": "Estados Unidos",
    "Russia": "Rússia"
}
df['País'] = df['Country'].map(nome_paises_pt)

df.rename(columns={
    'TB_Cases': 'Casos',
    'TB_Deaths': 'Mortes',
    'TB_Incidence_Rate': 'Incidência (%)',
    'TB_Mortality_Rate': 'Mortalidade (%)',
    'TB_Treatment_Success_Rate': 'Sucesso no Tratamento (%)'
}, inplace=True)

# === Função para gerar o HTML com botão "Voltar" ===
def gerar_html_com_botao():
    ano_recente = df['Year'].max()
    dados = df[df['Year'] == ano_recente]

    fig = px.choropleth(
        data_frame=dados,
        locations="Country",  # ainda em inglês para funcionar no mapa
        locationmode="country names",
        color="Casos",
        hover_name="País",  # nome em português no hover
        hover_data={
            "Mortes": True,
            "Incidência (%)": True,
            "Mortalidade (%)": True,
            "Sucesso no Tratamento (%)": True,
            "Country": False  # oculta o nome original em inglês
        },
        color_continuous_scale="Reds",
        title=f"Casos de Tuberculose - {ano_recente}"
    )
    fig.update_geos(showcountries=True, showcoastlines=True, projection_type="natural earth")

    # Adiciona botão "Voltar" no HTML
    fig_html = fig.to_html(full_html=True, include_plotlyjs='cdn')
    botao = """
    <button onclick="pywebview.api.voltar()" 
            style="position:fixed; top:10px; left:10px; z-index:9999;
                   background-color:#2196F3; color:white; padding:10px;
                   font-size:16px; border:none; border-radius:5px;">
        ← Voltar
    </button>
    """
    fig_html = fig_html.replace('<body>', f'<body>{botao}')

    with tempfile.NamedTemporaryFile(delete=False, suffix=".html", mode="w", encoding="utf-8") as tmpfile:
        tmpfile.write(fig_html)
        return tmpfile.name

# === Classe para tratar o clique no botão "Voltar" ===
class API:
    def voltar(self):
        subprocess.Popen(["python", "overview.py"])  # ou "python3" dependendo do ambiente
        webview.windows[0].destroy()

# === Criar e mostrar a janela ===
html_path = gerar_html_com_botao()
api = API()

webview.create_window("Mapa Interativo - Tuberculose", html_path, js_api=api)
webview.start()

os.remove(html_path)


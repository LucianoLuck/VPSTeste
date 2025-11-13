# prompt: prompt: criar um gráfico de barras embelezado para o dataframe df com meses de 2024 da DataLancamento no eixo x e soma de valor para os elementos de Codigo que começam do "3" e são diferentes de (302040100, 301010000, 302061300) e tem o quarto caractere de CodigoEvento diferente de "7" no eixo y

import pandas as pd
import matplotlib.pyplot as plt

# Definindo o caminho do arquivo CSV
caminho_arquivo = r'razao.csv'

# Lendo o arquivo CSV usando o pandas
try:
    df = pd.read_csv(caminho_arquivo)
    print("Arquivo importado com sucesso!")
    print(df.head())  # Exibe as primeiras linhas do dataframe
except FileNotFoundError:
    print("Arquivo não encontrado. Verifique o caminho e o nome do arquivo.")
except Exception as e:
    print(f"Ocorreu um erro ao importar o arquivo: {e}")

# Convert 'DataLancamento' to datetime objects if not already done
if not pd.api.types.is_datetime64_any_dtype(df['DataLancamento']):
    df['DataLancamento'] = pd.to_datetime(df['DataLancamento'])

# Filter data for 2024
df_2024 = df[df['DataLancamento'].dt.year == 2024].copy()

# Convert 'Codigo' and 'CodigoEvento' to strings for string operations
df_2024['Codigo'] = df_2024['Codigo'].astype(str)
df_2024['CodigoEvento'] = df_2024['CodigoEvento'].astype(str)

# Filter 'Codigo' and 'CodigoEvento'
codigos_filtrados = df_2024[
    (df_2024['Codigo'].str.startswith('3')) &
    (~df_2024['Codigo'].isin(['302040100', '301010000', '302061300'])) &
    (df_2024['CodigoEvento'].str.len() >= 4) &
    (df_2024['CodigoEvento'].str[3] != '7')
]

# Group by month and sum 'Valor'
monthly_sums = codigos_filtrados.groupby(codigos_filtrados['DataLancamento'].dt.month)['Valor'].sum()

# Create the embellished bar plot
plt.figure(figsize=(12, 6))  # Increased figure size
plt.bar(monthly_sums.index, monthly_sums.values, color='skyblue', edgecolor='black', linewidth=1.2) # Added color and edge
plt.xlabel('Mês de 2024', fontsize=14) # Increased font size for labels and title
plt.ylabel('Soma do Valor', fontsize=14)
plt.title('Soma do Valor por Mês para Códigos Filtrados em 2024', fontsize=16, fontweight='bold')
plt.xticks(monthly_sums.index, fontsize=12) # Customized x-axis ticks
plt.yticks(fontsize=12) # Customized y-axis ticks
plt.grid(axis='y', linestyle='--', alpha=0.7) # Added a grid for better readability
plt.gca().spines['top'].set_visible(False)  # Remove top and right spines
plt.gca().spines['right'].set_visible(False)

# Annotate bars with values
for i, v in enumerate(monthly_sums.values):
    plt.text(i, v + 5, str(round(v, 2)), ha='center', va='bottom', fontsize=10)  # Adjusted annotation position and size

plt.tight_layout() # Adjust layout to prevent labels from overlapping
plt.savefig('/srv/files/ProjetosPython/Teste/grafico.png')
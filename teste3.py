# Ativar o virtual enviroment para o projeto. A primeira vez o virtual enviroment é criado com "python3 -m venv myenv". Depois deve ser ativado com "source myenv/bin/activate" em /srv/files/ProjetosPython/projeto

# prompt: # prompt: criar uma tabela dinâmica que tenha nas linhas os Codigos que começam com 3 e são diferentes de (301010000,302040100, 302061300) e que o quarto caractere de CodigoEvento diferente de "7" nas colunas os anos de DataLancamento. Mostre ordenado por valor no ano de 2024. Mostre a soma dos anos

import pandas as pd

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

# Convert relevant columns to string type
df['Codigo'] = df['Codigo'].astype(str)
df['CodigoEvento'] = df['CodigoEvento'].astype(str)

# Filter the DataFrame
filtered_df = df[
    (df['Codigo'].str.startswith('3')) &
    (~df['Codigo'].isin(['301010000', '302040100', '302061300'])) &
    (df['CodigoEvento'].str[3] != '7') &
    (df['CodigoEvento'].str.len() >= 4)
]

# Create the pivot table
pivot_table = pd.pivot_table(filtered_df, values='Valor', index='Codigo', columns=filtered_df['DataLancamento'].dt.year, aggfunc='sum')

# Sort the pivot table by the values in the '2024' column (or another year if needed).
pivot_table_sorted = pivot_table.sort_values(by=2024, ascending=False)


# Display the sorted pivot table
print(pivot_table_sorted)

# Calculate the sum of values for each year.
year_sums = pivot_table.sum()

# Print the sum of values for each year.
print("\nSum of values for each year:")
year_sums

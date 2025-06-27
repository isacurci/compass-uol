import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def process_data(input_csv_path, output_dir):
    """
    Processa o CSV limpo, responde às perguntas e gera gráficos.
    """
    
    try:
        df = pd.read_csv(input_csv_path)
        print(f"'{input_csv_path}' carregado com sucesso para processamento.")
        print("Colunas disponíveis no DataFrame após carregamento:", df.columns.tolist())
    except FileNotFoundError:
        print(f"Erro: O arquivo '{input_csv_path}' não foi encontrado. Certifique-se de que o ETL foi executado corretamente e o arquivo foi gerado.")
        return
    except Exception as e:
        print(f"Erro ao carregar o arquivo '{input_csv_path}': {e}")
        return

    # Garante que o diretório de saída existe
    os.makedirs(output_dir, exist_ok=True)

    # --- Respostas às Perguntas ---
    answers = {}

    # Q1 - Qual é a artista que mais aparece nessa lista e possui a maior média de seu faturamento bruto (Actual gross)?
    artist_stats = df.groupby('Artist').agg(
        count=('Artist', 'size'),
        avg_actual_gross=('Actual gross', 'mean')
    ).sort_values(by=['count', 'avg_actual_gross'], ascending=[False, False])

    if not artist_stats.empty:
        q1_artist = artist_stats.index[0]
        answers['Q1'] = f"A artista que mais aparece e possui a maior média de faturamento bruto é: {q1_artist}"
    else:
        answers['Q1'] = "Dados insuficientes para determinar a artista para Q1."


    # Q2 - Das turnês que aconteceram dentro de um ano, qual a turnê com a maior média de faturamento bruto (Average gross)?
    df_one_year_tours = df[
        (df['End year'] - df['Start year'] <= 1) &
        (df['Average gross'].notna())
    ]
    if not df_one_year_tours.empty:
        q2_tour_info = df_one_year_tours.loc[df_one_year_tours['Average gross'].idxmax()]
        answers['Q2'] = (f"A turnê de um ano com a maior média de faturamento bruto é '{q2_tour_info['Tour title']}' "
                          f"(Artista: {q2_tour_info['Artist']}, Média: ${q2_tour_info['Average gross']:.2f})")
    else:
        answers['Q2'] = "Nenhuma turnê de um ano encontrada ou dados insuficientes para esta análise."


    # Q3 - Quais são as 3 turnês que possuem o show (unitário) mais lucrativo?
    # Utilize a coluna "Adjusted gross (in 2022 dollars)". 
    df['Profit per Show'] = df.apply(
        lambda row: row['Adjusted gross (in 2022 dollars)'] / row['Shows'] if row['Shows'] > 0 else 0,
        axis=1
    )

    df_valid_profit = df[(df['Adjusted gross (in 2022 dollars)'].notna()) & (df['Shows'] > 0)]

    if not df_valid_profit.empty:
        top_3_tours = df_valid_profit.sort_values(by='Profit per Show', ascending=False).head(3)
        q3_response = "As 3 turnês com o show unitário mais lucrativo são:\n"
        for index, row in top_3_tours.iterrows():
            q3_response += (f"- Tour: {row['Tour title']}, Artista: {row['Artist']}, "
                            f"Valor por Show: ${row['Profit per Show']:.2f}\n")
        answers['Q3'] = q3_response.strip()
    else:
        answers['Q3'] = "Nenhuma turnê com dados válidos para calcular o lucro por show."


    # --- Salvar respostas em respostas.txt ---
    respostas_path = os.path.join(output_dir, "respostas.txt")
    with open(respostas_path, "w", encoding='utf-8') as f:
        f.write(f"Q1:\n--- {answers['Q1']}\n\n")
        f.write(f"Q2:\n--- {answers['Q2']}\n\n")
        f.write(f"Q3:\n--- {answers['Q3']}\n")
    print(f"Respostas salvas em: {respostas_path}")

    # --- Geração de Gráficos ---

    # Q4 - Para a artista que mais aparece nessa lista e que tenha o maior somatório de faturamento bruto,
    # crie um gráfico de linhas que mostra o faturamento por ano da turnê (use a coluna Start Year).
    # Apenas os anos com turnês.

    artist_total_gross = df.groupby('Artist').agg(
        count=('Artist', 'size'),
        total_actual_gross=('Actual gross', 'sum')
    ).sort_values(by=['count', 'total_actual_gross'], ascending=[False, False])

    if not artist_total_gross.empty:
        artist_for_q4 = artist_total_gross.index[0]

        df_artist_q4 = df[df['Artist'] == artist_for_q4]
        yearly_gross_q4 = df_artist_q4.groupby('Start year')['Actual gross'].sum().reset_index()

        plt.figure(figsize=(12, 7))
        sns.lineplot(data=yearly_gross_q4, x='Start year', y='Actual gross', marker='o', color='purple')
        plt.title(f'Faturamento Bruto Total por Ano de Início da Turnê - {artist_for_q4}', fontsize=16)
        plt.xlabel('Ano de Início da Turnê', fontsize=12)
        plt.ylabel('Faturamento Bruto Total ($)', fontsize=12)
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.xticks(yearly_gross_q4['Start year'].unique(), rotation=45)
        plt.ticklabel_format(style='plain', axis='y')
        plt.tight_layout()
        q4_path = os.path.join(output_dir, "Q4.png")
        plt.savefig(q4_path)
        print(f"Gráfico Q4 salvo em: {q4_path}")
        plt.close()
    else:
        print("Não foi possível gerar Q4: Dados insuficientes para identificar a artista principal ou faturamento anual.")

    # Q5 - Faça um gráfico de colunas demonstrando as 5 artistas com mais shows na lista.
    # Correção para usar a coluna 'Shows' para a soma do número de shows
    top_5_artists_shows = df.groupby('Artist')['Shows'].sum().nlargest(5).reset_index()
    top_5_artists_shows.columns = ['Artist', 'Number of Shows'] # Já está correto

    if not top_5_artists_shows.empty:
        plt.figure(figsize=(12, 7))
        sns.barplot(data=top_5_artists_shows, x='Artist', y='Number of Shows', palette='viridis')
        plt.title('Top 5 Artistas por Número de Shows', fontsize=16)
        plt.xlabel('Artista', fontsize=12)
        plt.ylabel('Número de Shows', fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        q5_path = os.path.join(output_dir, "Q5.png")
        plt.savefig(q5_path)
        print(f"Gráfico Q5 salvo em: {q5_path}")
        plt.close()
    else:
        print("Não foi possível gerar Q5: Dados insuficientes para identificar as 5 artistas com mais shows.")

if __name__ == "__main__":
    process_data("output/csv_limpo.csv", "output") # Alterado para o caminho relativo dentro do WORKDIR /app
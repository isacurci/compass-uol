import pandas as pd
import os

def clean_data(input_csv_path, output_csv_path):
    """
    Carrega o CSV bruto, limpa os dados e salva um CSV limpo.
    """
    df = None
    encodings_to_try = ['utf-8', 'latin1', 'cp1252'] # Ordem de preferência para tentar encodings

    for encoding in encodings_to_try:
        try:
            # Tentar ler com o encoding atual e delimitador de vírgula (padrão)
            df = pd.read_csv(input_csv_path, encoding=encoding)
            print(f"'{input_csv_path}' carregado com sucesso usando encoding '{encoding}'.")

            # Verificar se a leitura resultou em apenas uma coluna, indicando delimitador errado
            if df.shape[1] == 1:
                print(f"Aviso: A leitura com '{encoding}' resultou em apenas uma coluna. Tentando com delimitador ';' e encoding '{encoding}'.")
                df = pd.read_csv(input_csv_path, sep=';', encoding=encoding)
                if df.shape[1] == 1:
                     print(f"Aviso: A leitura com ';' e '{encoding}' também resultou em apenas uma coluna. Verifique o delimitador e encoding reais do CSV.")
                     continue # Tenta o próximo encoding
                else:
                     print(f"Leitura com delimitador ';' e encoding '{encoding}' bem-sucedida.")
            break # Se a leitura foi bem-sucedida, sai do loop
        except FileNotFoundError:
            print(f"Erro: O arquivo de entrada '{input_csv_path}' não foi encontrado.")
            return # Sai da função se o arquivo não existe
        except UnicodeDecodeError:
            print(f"Erro de decodificação com encoding '{encoding}'. Tentando próximo...")
            continue # Tenta o próximo encoding
        except Exception as e:
            print(f"Erro inesperado ao carregar o arquivo '{input_csv_path}' com encoding '{encoding}': {e}")
            continue # Tenta o próximo encoding

    if df is None:
        print("Erro crítico: Não foi possível carregar o arquivo CSV com nenhuma das codificações tentadas.")
        return

    # --- Limpeza de Colunas Monetárias ---
    monetary_cols_original = ['Actual gross', 'Adjustedgross (in 2022 dollars)', 'Average gross']
    for col in monetary_cols_original:
        if col in df.columns:
            df[col] = df[col].astype(str).str.replace('$', '', regex=False).str.replace(',', '', regex=False).str.strip()
            df[col] = pd.to_numeric(df[col], errors='coerce')
            # **ADICIONADO: Força a coluna para tipo float**
            df[col] = df[col].astype(float)
        else:
            print(f"Aviso: Coluna monetária '{col}' não encontrada no DataFrame.")

    # --- Limpeza de 'Artist' e 'Tour title' (remover notas de rodapé) ---
    if 'Artist' in df.columns:
        df['Artist'] = df['Artist'].astype(str).str.replace(r'\[.*?\]', '', regex=True).str.strip()
    if 'Tour title' in df.columns:
        df['Tour title'] = df['Tour title'].astype(str).str.replace(r'[†‡\*\[].*?$', '', regex=True).str.strip()

    # --- Criação de 'Start year' e 'End year' a partir de 'Year(s)' ---
    if 'Year(s)' in df.columns:
        def parse_years(year_str):
            year_str = str(year_str).strip()
            if '-' in year_str:
                start, end = map(int, year_str.split('-'))
            else:
                start = end = int(year_str)
            return pd.Series([start, end])

        df[['Start year', 'End year']] = df['Year(s)'].apply(lambda x: parse_years(x) if pd.notna(x) else pd.Series([pd.NA, pd.NA]))
        df['Start year'] = pd.to_numeric(df['Start year'], errors='coerce').astype('Int64')
        df['End year'] = pd.to_numeric(df['End year'], errors='coerce').astype('Int64')
    else:
        print("Erro: Coluna 'Year(s)' não encontrada no DataFrame. 'Start year' e 'End year' não puderam ser criadas.")
        df['Start year'] = pd.NA
        df['End year'] = pd.NA

    # --- Garantir que 'Shows' é do tipo inteiro e tratar NaNs ---
    if 'Shows' in df.columns:
        df['Shows'] = df['Shows'].astype(str).str.replace(r'[^0-9]', '', regex=True)
        df['Shows'] = pd.to_numeric(df['Shows'], errors='coerce').fillna(0).astype(int)
    else:
        print("Aviso: Coluna 'Shows' não encontrada no DataFrame.")
        df['Shows'] = 0

    # --- Tratar valores nulos/NaNs após conversões ---
    # Aplica fillna(0) para as colunas numéricas que podem ter ficado NaN após pd.to_numeric.
    # Para colunas float, fillna(0) resultará em 0.0.
    for col in monetary_cols_original: # Apenas as colunas monetárias, 'Shows' já foi tratado.
        if col in df.columns:
            df[col] = df[col].fillna(0)

    # --- Renomear 'Adjustedgross (in 2022 dollars)' ---
    if 'Adjustedgross (in 2022 dollars)' in df.columns:
        df.rename(columns={'Adjustedgross (in 2022 dollars)': 'Adjusted gross (in 2022 dollars)'}, inplace=True)
    else:
        print("Aviso: Coluna 'Adjustedgross (in 2022 dollars)' não encontrada para renomear.")

    # --- Salvar o DataFrame limpo ---
    output_dir_path = os.path.dirname(output_csv_path)
    os.makedirs(output_dir_path, exist_ok=True)

    df.to_csv(output_csv_path, index=False, sep=',', float_format='%.1f')
    print(f"Dados limpos salvos em: {output_csv_path}")

if __name__ == "__main__":
    clean_data("data/concert_tours_by_women.csv", "output/csv_limpo.csv")
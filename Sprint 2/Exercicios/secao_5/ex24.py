def processar_notas(arquivo_csv):
    with open(arquivo_csv, 'r', encoding='utf-8') as f:
        linhas = f.readlines()

    estudantes = []

    for linha in linhas:
        partes = linha.strip().split(',')
        nome = partes[0].strip()
        notas = list(map(float, partes[1:]))
        maiores = sorted(notas, reverse=True)[:3]
        media = round(sum(maiores) / 3, 2)
        maiores = list(map(lambda x: int(x) if x == int(x) else x, maiores))
        estudantes.append((nome, maiores, media))

    estudantes.sort(key=lambda x: x[0])

    for nome, notas, media in estudantes:
        print(f"Nome: {nome} Notas: {notas} Média: {media:.2f}")

processar_notas('estudantes.csv')

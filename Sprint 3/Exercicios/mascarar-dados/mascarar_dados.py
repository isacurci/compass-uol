import hashlib
import sys

def gerar_hash_sha1(texto):
    # Codifica a string para bytes antes de aplicar o hash
    sha1_hash = hashlib.sha1(texto.encode('utf-8'))
    # Retorna o hash em formato hexadecimal
    return sha1_hash.hexdigest()

if __name__ == "__main__":
    print("Gerador de Hash SHA-1")
    print("Digite 'sair' para encerrar.")

    # Verifica se há argumentos de linha de comando
    if len(sys.argv) > 1:
        palavras = sys.argv[1:]
        for palavra in palavras:
            hash_gerado = gerar_hash_sha1(palavra)
            print(f"'{palavra}' (SHA-1): {hash_gerado}")
    else:
        # Loop infinito para receber inputs do usuário
        while True:
            entrada = input("Digite uma string: ")
            if entrada.lower() == 'sair':
                break
            hash_gerado = gerar_hash_sha1(entrada)
            print(f"'{entrada}' (SHA-1): {hash_gerado}")
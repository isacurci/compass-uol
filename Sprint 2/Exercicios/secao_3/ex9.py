# Implemente a classe Lampada. A classe Lâmpada recebe um booleano no seu construtor, Truese a lâmpada estiver ligada, False caso esteja desligada. A classe Lampada possuí os seguintes métodos:
# liga(): muda o estado da lâmpada para ligada
# desliga(): muda o estado da lâmpada para desligada
# esta_ligada(): retorna verdadeiro se a lâmpada estiver ligada, falso caso contrário
# Para testar sua classe:
# Ligue a Lampada
# Imprima: A lâmpada está ligada? True
# Desligue a Lampada
# Imprima: A lâmpada ainda está ligada? False

class Lampada: 
    def __init__(self, ligada): # construtor para inicialização
       
       # Construtor da classe Lampada.
       # Args:
          # ligada (bool): True se a lâmpada estiver ligada, False caso contrário.
            
        self.ligada = ligada  

    def liga(self): 
        # Muda o estado da lâmpada para ligada
        self.ligada = True # Atualiza o estado do atributo

    def desliga(self): # Muda o estado da lâmpada para desligada 
        self.ligada = False # usandoa s boas praticas: Atualiza o estado do atributo

    def esta_ligada(self): 
        # Retorna verdadeiro se a lâmpada estiver ligada, falso caso contrário.

        # Returns:
           # bool: True se a lâmpada estiver ligada, False caso contrário.
        return self.ligada # Retorna o valor do atributo

# Testando 
minha_lampada = Lampada(False) # Instanciação da classe
# Inicialmente desligada

# Ligue a Lâmpada
minha_lampada.liga() 

# Imprimir
print(f"A lâmpada está ligada? {minha_lampada.esta_ligada()}") # usandoa s boas praticas: Uso de f-strings para formatação e chamada de método para verificar o estado

# Desligue a Lâmpada
minha_lampada.desliga() 

# Imprimir
print(f"A lâmpada ainda está ligada? {minha_lampada.esta_ligada()}") 
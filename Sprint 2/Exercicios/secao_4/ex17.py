#Crie uma classe  Calculo  que contenha um método que aceita dois parâmetros, X e Y, e retorne a soma dos dois. Nessa mesma classe, implemente um método de subtração, que aceita dois parâmetros, X e Y, e retorne a subtração dos dois (resultados negativos são permitidos).


class Calculo:
    def somar(self, x, y):
        return x + y

    def subtrair(self, x, y):
        return x - y


# Testando
x = 4
y = 5

calc = Calculo()

print(f"Somando: {x}+{y} = {calc.somar(x, y)}")
print(f"Subtraindo: {x}-{y} = {calc.subtrair(x, y)}")

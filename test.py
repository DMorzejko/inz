import math
import random
# Definicja klasy
class Kolo:
    def __init__(self, promien):
        self.promien = promien
    def oblicz_pole(self):
        return math.pi * (self.promien ** 2)
kolo1 = Kolo(5)
pole_kola = kolo1.oblicz_pole()
print(f"Pole koła: {pole_kola:.2f}")
liczby = [random.randint(1, 100) for _ in range(10)]
print(f"Losowe liczby: {liczby}")
suma = 0
for liczba in liczby:
    suma += liczba

print(f"Suma liczb: {suma}")
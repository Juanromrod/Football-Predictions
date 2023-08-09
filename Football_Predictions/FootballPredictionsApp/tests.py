from django.test import TestCase
from footballData import calcular_doble_oportunidad, calcular_resultado_probable, calcular_probabilidad_apuesta

# Create your tests here.

#prob = [0.3, 0.3, 0.4]
#print(calcular_doble_oportunidad(prob))

local = [0.6, 0.3, 0.2], 0, 'X', [[0.4, 0.2, 0.3,(12,1.2)],[0.4, 0.2, 0.3,(12,1.2)],[0.4, 0.2, 0.3,(12,1.2)]]
visitante = [0.6, 0.3, 0.2], 0, 'Y', [[0.4, 0.2, 0.3,(12,1.2)],[0.4, 0.2, 0.3,(12,1.2)],[0.4, 0.2, 0.3,(12,2.2)]]

print(f'{calcular_resultado_probable(local,visitante)}')
print("Hola mundo!")
